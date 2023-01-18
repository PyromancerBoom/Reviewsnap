from flask import Flask, render_template, request
import pickle

import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import openai
import os
from time import time, sleep
import textwrap
import re


def FinalFunction(inputURLbyUser):

    HEADERS = ({'User-Agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/90.0.4430.212 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})

    # user define function
    # Scrape the data
    def getdata(url):
        r = requests.get(url, headers=HEADERS)
        return r.text

    def html_code(url):

        # pass the url
        # into getdata function
        htmldata = getdata(url)
        soup = BeautifulSoup(htmldata, 'html.parser')

        # display html code
        return (soup)

    input_url = inputURLbyUser
    temp1 = input_url.split("/", 6)

    # Finding Product Name
    soupProduct = html_code(input_url)
    product_input = ""
    for item in soupProduct.find_all("span", class_="a-size-large product-title-word-break"):
        product_input = product_input + item.get_text()
    product_input = product_input.strip()

    model_input_url = ""
    temp1[4] = "product-reviews"
    temp1[6] = "ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber="
    for i in range(0, 6):
        model_input_url += temp1[i]+"/"
    # print(model_input_url)

    # model_input_url+="ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(star=starx,page=pagex)
    # page=1
    # a-expander-content reviewText review-text-content a-expander-partial-collapse-content --> reviews, a-size-large product-title-word-break --> product title
    # stars - 100 - 3 : 1 : 1 : 1 : 3
    # a-row a-spacing-base a-size-base --> no. of reviews/star

    def cus_rev(soup):
        # find the Html tag
        # with find()
        # and convert into string
        data_str = ""

        for item in soup.find_all("span", class_="a-size-base review-text review-text-content"):
            data_str = data_str + item.get_text()

        result = data_str.split("\n")

        rev_data = result
        rev_result = []
        for i in rev_data:
            if i == "":
                pass
            else:
                rev_result.append(i)
        return (rev_result)

    def findNumberOfReviewsPerStar(urlx, starx):
        urlx += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
            star=starx, page="1")
        soupx = html_code(urlx)
        nostr = ""
        for item in soupx.find_all("div", class_="a-row a-spacing-base a-size-base"):
            nostr = nostr+item.get_text()
        xn = nostr.split()[3]
        xnn = xn.split(",")
        numStarReview = ""
        for i in xnn:
            numStarReview += i
        return int(numStarReview)

    def extractReviewsIntoText(urlxy):
        # OneStarReviews
        oneStarReviews = [""]
        twoStarReviews = [""]
        threeStarReviews = [""]
        fourStarReviews = [""]
        fiveStarReviews = [""]
        if oneStarNumberPages < 3:
            for i in range(1, oneStarNumberPages+1):
                urlxyz = urlxy
                urlxyz += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
                    star="one", page=str(i))
                soupxy = html_code(urlxyz)
                rev2 = ""
                for j in cus_rev(soupxy):
                    oneStarReviews[0] += j
                # oneStarReviews.append(rev2)
        else:
            for i in range(1, 4):
                urlxyz = urlxy
                urlxyz += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
                    star="one", page=str(i))
                soupxy = html_code(urlxyz)
                rev2 = ""
                for j in cus_rev(soupxy):
                    oneStarReviews[0] += j
                # print(rev2,"\n")
                # oneStarReviews.append(rev2)

        if twoStarNumberPages != 0:
            urlxyz = urlxy
            urlxyz += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
                star="two", page="1")
            soupxy = html_code(urlxyz)
            rev2 = ""
            for j in cus_rev(soupxy):
                twoStarReviews[0] += j
            # twoStarReviews.append(rev2)

        if threeStarNumberPages != 0:
            urlxyz = urlxy
            urlxyz += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
                star="three", page="1")
            soupxy = html_code(urlxyz)
            rev2 = ""
            for j in cus_rev(soupxy):
                threeStarReviews[0] += j
            # threeStarReviews.append(rev2)

        if fourStarNumberPages != 0:
            urlxyz = urlxy
            urlxyz += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
                star="four", page="1")
            soupxy = html_code(urlxyz)
            rev2 = ""
            for j in cus_rev(soupxy):
                fourStarReviews[0] += j
            # fourStarReviews.append(rev2)

        if fiveStarNumberPages < 3:
            for i in range(1, fiveStarNumberPages+1):
                urlxyz = urlxy
                urlxyz += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
                    star="five", page=str(i))
                soupxy = html_code(urlxyz)
                rev2 = ""
                for j in cus_rev(soupxy):
                    fiveStarReviews[0] += j
                # fiveStarReviews.append(rev2)
        else:
            for i in range(1, 4):
                urlxyz = urlxy
                urlxyz += "ref=cm_cr_unknown?ie=UTF8&filterByStar={star}_star&reviewerType=all_reviews&pageNumber={page}#reviews-filter-bar".format(
                    star="five", page=str(i))
                soupxy = html_code(urlxyz)
                rev2 = ""
                for j in cus_rev(soupxy):
                    fiveStarReviews[0] += j
                # fiveStarReviews.append(rev2)

        return [oneStarReviews, twoStarReviews, threeStarReviews, fourStarReviews, fiveStarReviews]

    def open_file(filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()

    # openai.api_key = " " Add KEY here

    def save_file(content, filepath):
        with open(filepath, 'w', encoding='utf-8') as outfile:
            outfile.write(content)

    # here, tokens is token limit
    def gpt3_completion(prompt, engine='text-davinci-003', temp=0.7, top_p=1.0, tokens=1000, freq_pen=0.5, pres_pen=0.5, stop=['<<END>>']):
        max_retry = 5
        retry = 0
        while True:
            try:
                response = openai.Completion.create(
                    engine=engine,
                    prompt=prompt,
                    temperature=temp,
                    max_tokens=tokens,
                    top_p=top_p,
                    frequency_penalty=freq_pen,
                    presence_penalty=pres_pen,
                    stop=stop)
                text = response['choices'][0]['text'].strip()
                text = re.sub('\s+', ' ', text)
                # filename = '%s_gpt3.txt' % time()
                # with open('gpt3_logs/%s' % filename, 'w') as outfile:
                #     outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
                return text
            except Exception as oops:
                retry += 1
                if retry >= max_retry:
                    return "GPT3 error: %s" % oops
                print('Error communicating with OpenAI:', oops)
                sleep(1)

    def beautifySummary(summary):
        a1 = summary.split("Strengths: ")
        strengths = "Strengths: " + a1[1].split("Weaknesses: ")[0]
        weaknesses = "Weaknesses: " + \
            a1[1].split("Weaknesses: ")[1].split("Functionality: ")[0]
        functionality = "Functionality: " + \
            a1[1].split("Weaknesses: ")[1].split(
                "Functionality: ")[1].split("Worthiness: ")[0]
        worthiness = "Worthiness: " + \
            a1[1].split("Weaknesses: ")[1].split(
                "Functionality: ")[1].split("Worthiness: ")[1]
        return (product_input, strengths, weaknesses, functionality, worthiness)
        #("\n"+"REVIEW SNAP: HELPING YOU MAKE BETTER DECISIONS IN A SNAP"+"\n"+"\n"+"Snap Review generated for: "+product_input+"\n"+"\n"+"Strengths: "+ strengths+"\n"+"Weaknesses: "+ weaknesses+"\n"+"Functionality: "+ functionality+"\n"+"Worthiness: "+ worthiness+"\n")

    oneStarNumberPages = findNumberOfReviewsPerStar(model_input_url, "one")//10
    twoStarNumberPages = findNumberOfReviewsPerStar(model_input_url, "two")//10
    threeStarNumberPages = findNumberOfReviewsPerStar(
        model_input_url, "three")//10
    fourStarNumberPages = findNumberOfReviewsPerStar(
        model_input_url, "four")//10
    fiveStarNumberPages = findNumberOfReviewsPerStar(
        model_input_url, "five")//10

    # print("1:",oneStarNumberPages)
    # print("2:",twoStarNumberPages)
    # print("3:",threeStarNumberPages)
    # print("4:",fourStarNumberPages)
    # print("5:",fiveStarNumberPages)

    a = extractReviewsIntoText(model_input_url)
    alltext = ""
    for i in a:
        alltext += i[0]
        # print("--------------------")
    # 4 reviews per chunk! taking avg length to be 500 words. We need 70/4 = 17.5 chunks summarized, then again summarized. Check length of each, len * 0.25 for token size.

    # print(len(alltext))
    chunks = textwrap.wrap(alltext, 4000)
    result = list()
    # p = open_file("prompt.txt")
    promptText1 = """ Produce a summary of the following reviews. Classify your summary into strengths, weaknesses, functionality and worthiness without redundancy:
<<SUMMARY>>
SUMMARY HIGHLIGHTING KEY STRENGTHS, WEAKNESSES, FUNCTIONALITY, WORTHINESS: """

    count = 0
    for chunk in chunks:
        count = count + 1
        # open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = promptText1.replace('<<SUMMARY>>', chunk)
    #     prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt3_completion(prompt)
        #print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        result.append(summary)
    # save_file('\n\n'.join(result), 'output_%s.txt' % time())

    result = '\n\n'.join(result)

    promptText2 = """ Classify your summary into strengths, weaknesses, functionality and worthiness with NO repitition or redundancy:
<<SUMMARY>>
NON-REDUNDANT AND NON-CONFLICTING SUMMARY HIGHLIGHTING KEY STRENGTHS, WEAKNESSES, FUNCTIONALITY, WORTHINESS: """

    if (len(result)*0.25) < 3000:
        summaryFinal = gpt3_completion(
            promptText2.replace('<<SUMMARY>>', result))
        # print()
        # print("SUMMARY by result1:",beautifySummary(summaryFinal))
        summaryFinal = beautifySummary(summaryFinal)
        return summaryFinal
    else:
        result_chunks = textwrap.wrap(result, 4000)
        result2 = list()
        for result_chunk in result_chunks:
            result_chunk_summary = gpt3_completion(
                promptText2.replace('<<SUMMARY>>', result_chunk))
            result2.append(result_chunk_summary)
        result2 = '\n\n'.join(result2)
        summaryFinal = gpt3_completion(
            promptText2.replace('<<SUMMARY>>', result2))
        print()
        # print("SUMMARY by result2:",beautifySummary(summaryFinal))
        summaryFinal = beautifySummary(summaryFinal)
        return summaryFinal


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('../index.html')


#model = pickle.load(open('ReviewSnap.py', 'rb'))


@app.route('/predict', methods=['POST'])
def predict():
    link = request.form['link']
    # the link is then passed to the ML Code which returns an output stored in a variable
    # this variable x will be put inside prediction = x
    a, b, c, d, e = FinalFunction(link)
    return render_template('../predict.html', a=a, b=b, c=c, d=d, e=e,)


if __name__ == '__main__':
    app.run()
