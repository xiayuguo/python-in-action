import time
import pickle
import requests

zimu_map = {0: "A", 1: "B", 2: "C", 3: "D"}

question_list = []

current_index = 0

url = "https://mlearning.pingan.com.cn/learn/app/clientapi/exam/getExamPaper.do"

payload = "examId=02456&umId=526D217C55DA0E3FE054022128574717&sid=4B081A8901AE4BABB48148AC1B26D00E"
headers = {
    'content-type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    }
proxies = {
  "http": "localhost:8888",
  "https": "localhost:8888"
}

for i in range(1000):
    try:
        response = requests.request("POST", url, data=payload, headers=headers,
                                    proxies=proxies, verify=r"FiddlerRoot.crt")

        result = response.json()
        body = result["body"]
        exam_list = body["examArr"]

        with open("monikaoshi.txt", "a") as f:
            for element in exam_list:
                if isinstance(element, dict):
                    print(element["questionId"])
                    if element["questionId"] not in question_list:
                        current_index += 1
                        exam_list.append(element["questionId"])
                        f.write("%s. %s\n" % (current_index, element["question"]))
                        for i, ele in enumerate(element["sectionArr"]):
                            f.write("%s. %s " % (zimu_map[i], ele["sectionText"]+"(%s)" % ele["isCorrect"]))
                        f.write("\n")
            f.write("=====******************************************************======\n")
                            
    except Exception as e:
        print("error: %s" % str(e))
        print("closed at index: %s" % i)
        print("increase to %s" % current_index)
    time.sleep(30)
