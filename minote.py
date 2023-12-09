import requests
import os
import json
from urllib.parse import unquote
import argparse

global save_dir
# 小米云服务笔记 API URL
API_URL = 'https://i.mi.com/note/full/page/'
counter=1

def get_notes(cookie):
    headers = {'Cookie': unquote(cookie)}
    response = requests.get(API_URL, headers=headers)
    if response.status_code != 200:
        raise Exception('Failed to fetch data from API')

    return response.json().get('data', {}).get('entries', [])

def parse_extra_info(note):
    extra_info = note.get('extraInfo', '{}')
    try:
        return json.loads(extra_info)
    except json.JSONDecodeError:
        return {}

def get_note_content(note_id, cookie):
    note_url = f"https://i.mi.com/note/note/{note_id}"
    headers = {'Cookie': unquote(cookie)}
    response = requests.get(note_url, headers=headers)
    if response.status_code != 200:
        raise Exception('Failed to fetch note content from API')
    extraInfo=response.json().get('data', {}).get('entry', {}).get('extraInfo', {})
    title_json=json.loads(extraInfo)
    title=title_json.get('title')
    content= response.json().get('data', {}).get('entry', {}).get('content', '')
    return title,content
def sanitize_filename(title):
    # 替换或移除不合法字符
    safe_title = "".join([c if c.isalnum() or c in [' ', '_', '-'] else '' for c in title])
    return safe_title

def create_unique_filename(title, note_id, save_dir,noteID):
    global counter
    base_filename = f"{title}.md"
    filename = base_filename
    # 检查文件是否已存在，如果是，则添加序号
    if os.path.exists(os.path.join(save_dir, filename)):
        print(os.path.join(save_dir, filename))
        if note_id in noteID:
            filename = f"{title}.md"
        else:
            filename = f"{title}{counter}.md"
            counter += 1
    return filename

def save_as_markdown(note, data, save_dir,noteId):
    note_id = note.get('id')
    title, content = data
    content = content.replace('<text indent="1">', '').replace('</text>', '').replace('\n', '\n').replace('<b>','**').replace('</b>','**')\
        .replace('<background color="#9affe8af">','<span style="background-color: rgba(98,0,238,0.06)>').replace('</background>','</span>')
    # 如果标题为空，从内容中提取前30个字符作为标题
    if not title:
        title = content[:30].strip()  # 从内容中提取前30个字符并去除前后空白
        title = title.split('\n', 1)[0]  # 只取第一行作为标题
    safe_title = sanitize_filename(title)

    markdown_text = content
    print(content)
    file_name = create_unique_filename(safe_title, note_id, save_dir,noteId)
    file_path = os.path.join(save_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(markdown_text)

def main():
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    notes = get_notes(minote_cookie)
    for note in notes:
        note_id = note.get('id')
        noteId_str = ', '.join(map(str, noteId))
        with open('data.txt', 'w') as file:
            file.write(noteId_str)
        content = get_note_content(note_id, minote_cookie)
        save_as_markdown(note, content, save_dir,noteId)
        if note_id not in noteId:
            noteId.append(note_id)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("minote_cookie")
    parser.add_argument("save_dir")
    options = parser.parse_args()
    minote_cookie = options.minote_cookie
    save_dir=options.save_dir
    if os.path.exists('data.txt') and os.path.getsize('data.txt') > 0:
        with open('data.txt', 'r') as file:
            noteIdStr = file.read()
        noteId = noteIdStr.split(', ')
        noteId = list(map(int, noteId))
        print(noteId)
    main()

