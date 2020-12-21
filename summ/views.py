from django.shortcuts import render
from .models import Services
import speech_recognition as sr
from Algorithmia import client
from django.core.mail import EmailMessage
import bs4 as bs
import urllib.request
import re
import heapq
import nltk
import moviepy.editor as me
import bs4 as bs
import urllib.request
import re
import heapq
import nltk
import sys
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence
import moviepy.editor as mp

def portfolio(request):
    return render(request, 'portfolio.html')

def send_mail(request):
    if request.method == "POST":
        email_id = request.POST['email_id']
        email = EmailMessage('Summarized textfile', 'Please find the attachment below.Thank you for valuing you time on our website.',
                             "summarygenerator1@gmail.com", [email_id])
        email.content_subtype = 'html'

        file = open("summ/static/"+"summarized_file.txt", 'r')
        email.attach("summ/static/"+"summarized_file.txt",
                     file.read(), 'text/plain')

        email.send()
        return render(request, 'summary.html')


def summ(request):
    serv = Services.objects.all()
    return render(request, 'summary.html', {'serv': serv})


#text summarizer

def text(request):
    return render(request, 'text.html')

 
def textop(request):
    if request.method == "POST":
        article_text = str(request.FILES["file"].read(), 'utf-8')
        n = int(request.POST['sent_no'])
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        maximum_frequncy = max(word_frequencies.values())
        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        summary_sentences = heapq.nlargest(
            n, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        file = 'summ/static/'+'summarized_file.txt'
        with open(file, 'w') as filetowrite:
            filetowrite.write(summary)
    return render(request, 'result.html', {'input': str(article_text), 'result': summary})


#audio summarizer

def audio(request):
    return render(request, 'audio.html')

def audioop(request):
    if request.method == 'POST':
        filename = request.FILES['file']
        r = sr.Recognizer()
        with sr.AudioFile(filename) as source:
            audio_data = r.record(source)
            text2 = r.recognize_google(audio_data)
            summarization_algorithm = client(
                "simFaH42Oe6xcB+ny9tjF+TiYdk1").algo("nlp/Summarizer/0.1.6")
            sent_no = int(request.POST['sent_no'])
            VALID = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM:;_-,.!?()']%$@ \n"
            text2 = ''.join(char for char in text2 if char in VALID)
            text2.replace('\n', ' ')
            text2 = ' '.join(text2.split())
            summary1 = summarization_algorithm.pipe([text2, sent_no]).result
            file = 'summ/static/'+'summarized_file.txt'
            with open(file, 'w') as filetowrite:
                filetowrite.write(summary1)
    return render(request, 'exmple.html', { 'result': summary1})




    





# wiki summarizer

def wiki(request):
    return render(request, "wiki.html")


def wikiop(request):
    if request.method == 'POST':
        filename = request.POST['wiki1']
        scraped_data = urllib.request.urlopen(filename)
        article = scraped_data.read()

        parsed_article = bs.BeautifulSoup(article, 'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
                    maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
            sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores.keys():
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]
        n = int(request.POST['sent_no'])
        summary_sentences = heapq.nlargest(
            n, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)
        file = 'summ/static/'+'summarized_file.txt'
        with open(file, 'w') as filetowrite:
            filetowrite.write(summary)
    return render(request, "wikiop.html", {'result': summary})



def video(request):
    return render(request, "video.html")

def vidop(request):
    if request.method == 'POST':
        filename = request.FILES['video']
        clip = mp.VideoFileClip("video1.mp4")
        clip.audio.write_audiofile(r"converted.wav")
        r = sr.Recognizer()
        r = sr.Recognizer()
        # open the audio file using pydub
        sound = AudioSegment.from_wav("converted.wav")
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = 500,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
        )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            # recognize the chunk
            with sr.AudioFile(chunk_filename) as source:
                audio_listened = r.record(source)
                # try converting it to text
                try:
                    text = r.recognize_google(audio_listened)
                except sr.UnknownValueError as e:
                    print("Error:", str(e))
                else:
                    text = f"{text.capitalize()}. "
                    #print(chunk_filename, ":", text)
                    whole_text += text
        # return the text for all chunks detected
        x = open("vidsum.txt", 'w')
        x.write(whole_text)
        x.close()
        
        #article = open(file,"r")
        scraped_data = open("vidsum.txt","r")
        #scraped_data.read([file])
        article = scraped_data.read()
        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text
        #article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        #article_text = re.sub(r'\s+', ' ', article_text)
        sentence_list = nltk.sent_tokenize(article_text)
        stopwords = nltk.corpus.stopwords.words('english')

        word_frequencies = {}
        for word in nltk.word_tokenize(article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
                    maximum_frequncy = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word]/maximum_frequncy)
            sentence_scores = {}
        for sent in sentence_list:
                for word in nltk.word_tokenize(sent.lower()):
                    if word in word_frequencies.keys():
                        if len(sent.split(' ')) < 30:
                            if sent not in sentence_scores.keys():
                                sentence_scores[sent] = word_frequencies[word]
                            else:
                                sentence_scores[sent] += word_frequencies[word]
        summary_sentences = heapq.nlargest(10, sentence_scores, key=sentence_scores.get)
        file = "vidsum.txt"
        summary = ' '.join(summary_sentences)
        summary_filename = file.split(".")[0] + "summary.txt"
        y = open(summary_filename, 'w')
        y.write(". ".join(summary_sentences))
        y.close()

        f = open("vidsum.txt", "r")
        result=f.read()
    return render(request, "vidop.html",{'result':result}) 