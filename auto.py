# -*- coding: utf-8 -*-
# 檔案名稱: auto.py
# 作者: 41243144
# 日期: 2025/04/22
# 版本: 1.0.0
# 說明: 
#   這是一個自動化測試程式，主要功能是遍歷指定資料夾中的所有檔案，
#   對每個檔案執行測試邏輯，並將測試結果輸出到指定的結果資料夾中。
#   程式適用於需要批次處理檔案的情境，例如測試腳本、資料驗證或格式檢查。
#   此程式的設計目的是提高測試效率，減少人工操作。
#
# 功能:
#   1. 自動掃描指定資料夾中的檔案(自動搜尋主程式)。
#   2. 對每個檔案執行測試或處理邏輯。
#   3. 將測試結果以結構化的方式輸出到結果資料夾。
#
# 使用方式:
#   - 將此程式放置於專案目錄中，並設定相關資料夾路徑。
#   - 可根據需求修改測試邏輯或輸出格式。
#
# 注意事項:
#   - 確保資料夾路徑正確，且具有讀寫權限。
#   - 測試邏輯需根據實際需求進行擴展。
#
# JSON 格式:
#   {
#       "結果": {
#           "學號": {
#               "result": "✅ OK" / "❌ Error"
#           }
#       },
#
#       "詳細內容": {
#           "檔案名稱": {
#               "正確輸出": "正確的輸出結果",
#               "學號": {
#                   "result": "✅ OK" / "❌ Error",
#                   "output": "執行結果",
#                   "file_path": "file:///path/to/file"
#               }
#           }
#       }
#   }
#
#
# 參數: 無

import subprocess
import os
import hashlib
import json


ENCCODING = 'utf-8'
INPUT_FOLDOR = os.path.join(os.getcwd(), 'input')
ANSWERS_FOLDOR = os.path.join(os.getcwd(), 'answers')
DATA_SET_FOLDER = os.path.join(os.getcwd(), 'dataset')
OUTPUT_FOLDER = os.path.join(os.getcwd(), 'output')

COMMAND = {
    '.py' : 'python',
    '.java' : 'java',
    '.cpp' : 'g++',
    '.c' : 'gcc',
}

MAIN_COMMAND = {
    '.py' : '__main__',
    '.java' : 'public static void main',
    '.cpp' : 'int main',
}

TIME_OUT = 1

def read_floder_file(file_path : str) -> dict:
    """
    Reads a file and returns its content as a dictionary.
        :param file_path: Path to the file to be read.
        :return: Dictionary containing the file content.
    """
    data = {}
    for root, _, files in os.walk(file_path):
        for file in files:
            full_path = os.path.join(root, file)
            data[file] = full_path
    return data

def read_floder_list(file_path: str) -> list:
    """
    Reads a directory and returns a list of subdirectories.
        :param file_path: Path to the directory to be read.
        :return: List containing the names of subdirectories.
    """
    folders = []
    for root, dirs, _ in os.walk(file_path):
        for dir_name in dirs:
            full_path = os.path.join(root, dir_name)
            folders.append(full_path)
    return folders


def read_file(file_path: str) -> str:
    """
    Reads a file and returns its content as a string.
        :param file_path: Path to the file to be read.
        :return: Content of the file as a string.
    """
    with open(file_path, 'r', encoding=ENCCODING) as f:
        content = f.read()
    return content

def write_file(file_name : str, output : dict) -> None:
    """
    Writes content to a file.
        :param file_path: Path to the file to be written.
        :param content: Content to be written to the file.
    """
    output_file_path = os.path.join(OUTPUT_FOLDER, f"{file_name}.json")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    with open(output_file_path, 'w', encoding=ENCCODING) as f:
        json.dump(output, f, indent=4, ensure_ascii=False)
    print(f"Output saved to {output_file_path}")

def generate_hash_key(data: str) -> dict:
    """
    Generates a hash key for the given data.
        :param data: Data to be hashed.
        :return: Dictionary containing the hash key.
    """
    hash_key = hashlib.sha256(data.encode()).hexdigest()
    return hash_key

    

def run_command(command: str, input_data : str=None) -> str:
    """
    Runs a shell command and returns its output.
        :param command: Shell command to be executed.
        :return: Output of the command.
    """
    try:
        result = subprocess.run(
            command,
            input=input_data or "",
            shell=True,
            capture_output=True,
            text=True,
            timeout=TIME_OUT
        )

        if result.returncode != 0:
            return f"Error: {result.stderr}"
        else:
            return result.stdout
    except subprocess.TimeoutExpired:
        return "Error: Command timed out."

def main():
    """
    Main function to execute the script.
    """
    input_data = {}
    answers_data = {}
    dataset_data = {}

    #-------------------------------------------------------------------------
    # Check if the input file exists
    if os.path.exists(INPUT_FOLDOR):
        # Read the input file
        input_data = read_floder_file(INPUT_FOLDOR)
    else:
        print(f"⚠️  Input folder {INPUT_FOLDOR} does not exist.")

    # Check if the answers folder exists
    if os.path.exists(ANSWERS_FOLDOR):
        # Read the answers file
        answers_data = read_floder_file(ANSWERS_FOLDOR)
    else:
        print("⚠️  Answers folder does not exist:", ANSWERS_FOLDOR)

    # Check if the dataset folder exists
    if os.path.exists(DATA_SET_FOLDER):
        # Read the dataset file
        dataset_data = read_floder_list(DATA_SET_FOLDER)
    else:
        print("⚠️  Dataset folder does not exist:", DATA_SET_FOLDER)
    #-------------------------------------------------------------------------
    # Check if the input data, answers data, and dataset data are empty
    if not input_data:
        print("⚠️  No input data found.")

    if not answers_data:
        print("⚠️  No answers data found.")

    if not dataset_data:
        print("❌  No dataset data found.")
        return

    if len(input_data) != len(answers_data):
        print("❌ Input and answers data do not match.")
    
    # print("Input data:", input_data)
    # print("Answers data:", answers_data)
    # print("Dataset data:", dataset_data)
    dataset_data = sorted(dataset_data, key=lambda x: os.path.basename(x))
    #-------------------------------------------------------------------------
    output = {}
    output['結果'] = {}
    output['詳細內容'] = {}
    # Check if the input data and answers data are not empty
    if input_data:
        # Iterate through the input data and answers data
        for file_name, file_path in input_data.items():
            if file_name not in answers_data:
                print(f"❌  {file_name} not found in answers data.")
                continue
            
            print(f"--" * 20)
            print(f"Processing {file_name}...")

            answer = read_file(answers_data[file_name])
            input_data = read_file(file_path)

            output['詳細內容'][file_name] = {}
            output['詳細內容'][file_name]['正確輸出'] = answer

            answers_hash = generate_hash_key(answer)

            # Iterate through the dataset data
            for student_floder_path in dataset_data:
                student_files = read_floder_file(student_floder_path)
                studient_id = os.path.basename(student_floder_path)

                if studient_id not in output['結果']:
                    output['結果'][studient_id] = {"result" : "✅ OK"}
                output['詳細內容'][file_name][studient_id] = {}

                output['詳細內容'][file_name][studient_id]['result'] = "❌  Error"

                output['詳細內容'][file_name][studient_id]['output'] = "Not Found File"
               
                
                for student_file_name, student_file_path in student_files.items():
                    _, ext = os.path.splitext(student_file_name)
                    if ext not in COMMAND:
                        continue

                    file_content = read_file(student_file_path)
                    if MAIN_COMMAND.get(ext) not in file_content:
                        continue
                    output['詳細內容'][file_name][studient_id]['file_path'] = f"file:///{student_floder_path.replace(os.sep, '/')}"
                    
                    command = f"{COMMAND[ext]} {student_file_path}"
                    result = run_command(command, input_data)

                    result_hash = generate_hash_key(result)

                    if result_hash != answers_hash:
                        output['結果'][studient_id] = {"result" : "❌  Error"}
                        output['詳細內容'][file_name][studient_id]['result'] = "❌  Error"
                        print(f"❌  {studient_id} : Error")
                    else:
                        output['詳細內容'][file_name][studient_id]['result'] = "✅ OK"
                        print(f"✅  {studient_id} : OK")
                
                    output['詳細內容'][file_name][studient_id]['output'] = result
                    
        

    else:
        print("⚠️  No input data found.")
        for file_name, file_path in answers_data.items():
            answer = read_file(file_path)
            answer_hash = generate_hash_key(answer)
            
            output['結果'] = {}
            output['詳細內容'][file_name] = {}
            output['詳細內容'][file_name]['正確輸出'] = answer

            for student_floder_path in dataset_data:
                student_files = read_floder_file(student_floder_path)
                studient_id = os.path.basename(student_floder_path)

                if studient_id not in output['結果']:
                    output['結果'][studient_id] = {"result" : "✅ OK"}
                output['詳細內容'][file_name][studient_id] = {}
                output['詳細內容'][file_name][studient_id]['result'] = "Error"
                output['詳細內容'][file_name][studient_id]['output'] = "Not Found File"

                for student_file_name, student_file_path in student_files.items():
                    _, ext = os.path.splitext(student_file_name)
                    if ext not in COMMAND:
                        continue

                    file_content = read_file(student_file_path)
                    if MAIN_COMMAND.get(ext) not in file_content:
                        continue

                    output['詳細內容'][file_name][studient_id]['file_path'] = f"file:///{student_file_path.replace(os.sep, '/')}"
                    
                    command = f"{COMMAND[ext]} {student_file_path}"
                    result = run_command(command, answer)

                    result_hash = generate_hash_key(result)

                    if result_hash != answer_hash:
                        output['結果']['result'] = "❌  Error"
                        output['詳細內容'][file_name][studient_id]['result'] = "Error"
                        print(f"❌  {studient_id} : Error")
                    else:
                        output['詳細內容'][file_name][studient_id]['result'] = "OK"
                        print(f"✅  {studient_id} : OK")

                    output['詳細內容'][file_name][studient_id]['output'] = result
    
        write_file("自動批改結果", output)
    #-------------------------------------------------------------------------

if __name__ == "__main__":
    main()