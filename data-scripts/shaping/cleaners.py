import re
from typing import AnyStr, List

def remove_preface_and_postscript(text:str) -> AnyStr:
    return "\r\n".join(text.split("\r\n\r\n")[1:-1])

def remove_explanation(text:str) -> AnyStr:
    text = re.sub(r"----+[\s\S]+----+", "", text)
    return text

def remove_ctrl_char(text:str) -> AnyStr:
    return re.sub(r"［.*?］", "", text)

def remove_ruby(text:str) -> AnyStr:
    text = re.sub(r"\｜", "", text)
    return re.sub(r"《.*?》", "", text)

def remove_others(text:str) -> AnyStr:
    text = re.sub(r"〔〕", "", text)
    text = re.sub(r"[…×―※]", "", text)
    text = re.sub(r"「」", "", text)
    return text


def normalize_text(text:str) -> AnyStr:
    text = remove_preface_and_postscript(text)
    text = remove_explanation(text)
    text = remove_ctrl_char(text)
    text = remove_ruby(text)
    text = remove_others(text)
    return text