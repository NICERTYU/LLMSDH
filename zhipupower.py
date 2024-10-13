import streamlit as st
import time
from zhipuai import ZhipuAI
import os
import zipfile
import tarfile
import tempfile
import chardet
import markdown
import git
from github import Github
import requests
import shutil
import subprocess
import os
from urllib.parse import urlparse
import shutil
import os


def metagpt_generate_code(instruction):
    command = ['metagpt', instruction]
    subprocess.run(command, capture_output=True, text=True)
    

def zip_and_remove_other_folder(workspace_dir, exclude_folder):
    current_dir = os.getcwd()
    workspace_path = os.path.join(current_dir, workspace_dir)

    if not os.path.exists(workspace_path):
        st.error(f"目录 '{workspace_dir}' 不存在。")
        return None

    folders = [
        f for f in os.listdir(workspace_path) 
        if os.path.isdir(os.path.join(workspace_path, f)) and f != exclude_folder
    ]

    if len(folders) != 1:
        st.error(f"workspace 目录中必须只有一个文件夹，且不包括 '{exclude_folder}'。")
        return None

    folder_to_zip = folders[0]
    folder_to_zip_path = os.path.join(workspace_path, folder_to_zip)

    output_zip_name = f"{folder_to_zip}.zip"
    output_path = os.path.join(current_dir, output_zip_name)

    shutil.make_archive(output_path[:-4], 'zip', folder_to_zip_path)
    shutil.rmtree(folder_to_zip_path)
    
    return output_path



def delete_zip_file(file_path):
    """下载后删除 ZIP 文件的函数"""
    if os.path.exists(file_path):
        os.remove(file_path)
        st.session_state.zip_file_path = None  # 清除状态中的文件路径
        st.success("ZIP 文件已删除。")




def zip_and_remove_unique_folder(workspace_dir):
    # 获取当前工作目录
    current_dir = os.getcwd()

    # 构建 workspace 目录的完整路径
    workspace_path = os.path.join(current_dir, workspace_dir)

    # 检查 workspace 目录是否存在
    if not os.path.exists(workspace_path):
        print(f"目录 '{workspace_dir}' 不存在。")
        return

    # 获取 workspace 目录下的所有文件夹
    folders = [f for f in os.listdir(workspace_path) if os.path.isdir(os.path.join(workspace_path, f))]

    # 检查是否存在唯一一个文件夹
    if len(folders) != 1:
        print("workspace 目录中必须只有一个文件夹。")
        return

    # 获取唯一文件夹的名称
    unique_folder = folders[0]
    unique_folder_path = os.path.join(workspace_path, unique_folder)

    # 打包文件夹
    output_zip_name = f"{unique_folder}.zip"
    shutil.make_archive(os.path.join(current_dir, output_zip_name[:-4]), 'zip', unique_folder_path)

    # 删除文件夹
    shutil.rmtree(unique_folder_path)
    print(f"文件夹 '{unique_folder}' 已成功打包为 '{output_zip_name}' 并被删除。")
    return output_zip_name





openai_api_key = "067fbd5dd8562afc49b98b14efc3896e.LCpVekU5PwIdoGZY"

def read_file_encoding(file_path):
    # 检测文件编码
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    return encoding

def metagpt_generate_code(instruction):
    comand = ['metagpt', instruction, '--code-review', '--investment', '5', '--run-tests', '--n-round','6']
    result = subprocess.run(comand)



def get_repo_name(github_url):
    # 解析 URL，获取仓库路径
    parsed_url = urlparse(github_url)
    
    # 获取路径的最后一部分，即仓库名
    repo_name = os.path.basename(parsed_url.path)
    
    # 去掉.git后缀（如果有）
    if repo_name.endswith(".git"):
        repo_name = repo_name[:-4]
    
    return repo_name

def chatbot_page():  
        st.title("💬 LLMSDH: 软件原型开发平台")
        st.caption("🚀 A Streamlit LLMSDH: 软件原型开发平台 powered by 智谱清言")
        # Streamlit 代码



        prompt = st.text_input("输入指令：")
        if st.button("生成代码并打包文件"):
    # 调用函数生成代码
               metagpt_generate_code(prompt)

           
               st.success("代码生成成功！")
        
              # 打包并删除 workspace 中的唯一文件夹（排除 'storage' 文件夹）
               zip_file_path = zip_and_remove_other_folder("workspace", "storage")
        
               if zip_file_path:
            # 在会话状态中存储 ZIP 文件路径
                   st.session_state.zip_file_path = zip_file_path
            
                     # 提供下载按钮
                   with open(zip_file_path, "rb") as f:
                          st.download_button(
                          label="下载 ZIP 文件",
                          data=f,
                                file_name=os.path.basename(zip_file_path),
                                mime="application/zip",
                                on_click=lambda: delete_zip_file(st.session_state.zip_file_path)  # 下载后删除文件
                            )
           

            

def CodeGeeXIntrepreting():  
    from  jsonformat import analyze_project_profile
    st.title("🦜🔗 LLMSDH: 软件系统介绍开发平台")  
    st.caption("🚀 A Streamlit LLMSDH: 软件系统介绍开发平台 powered by 智谱清言")

    # 初始化会话状态
    if "codegeex_intrepreting_messages" not in st.session_state:
        st.session_state["codegeex_intrepreting_messages"] = []

    # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    if "code_update_projects" not in st.session_state:
        st.session_state["code_update_projects"] = []
    
    if "code_github_urls" not in st.session_state:
        st.session_state["code_github_urls"] = []

     # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    # 显示历史消息
    with message_placeholder.container():
        for message in st.session_state["codegeex_intrepreting_messages"]:
            if "project_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (来自项目: {message['project_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])

    # GitHub 链接输入框
    github_url = st.text_input("输入 GitHub 项目链接")

    # 上传文件或通过 GitHub 下载项目
    uploaded_project = st.file_uploader("或者上传项目文件", type=("zip", "tar", "tar.gz", "tar.bz2"), accept_multiple_files=True)
    
    # 检查 GitHub 链接是否为新的
    if github_url and github_url not in st.session_state["code_github_urls"]:
        st.session_state["code_github_urls"].append(github_url)  # 记录新的 GitHub 链接
        
        # 下载 GitHub 项目
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = download_github_repo(github_url, temp_dir)
            if repo_dir:
                analyze_project_profile(repo_dir, message_placeholder, get_repo_name(github_url))

    if uploaded_project:
        # 仅对新上传的项目进行处理
        new_projects = [project for project in uploaded_project if project.name not in st.session_state["code_update_projects"]]
        
        for project in new_projects:
            with tempfile.TemporaryDirectory() as temp_dir:
                if project.name.endswith('.zip'):
                    with zipfile.ZipFile(project, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                elif project.name.endswith(('.tar', '.tar.gz', '.tar.bz2')):
                    with tarfile.open(project, 'r') as tar_ref:
                        tar_ref.extractall(temp_dir)
                analyze_project_profile(temp_dir, message_placeholder, project.name)




    


    
    
    





def SoftwareEngineerDefectDetection():
    st.title("📝 LLMSDH: 快速短代码检测平台")
    st.caption("🚀 A Streamlit LLMSDH: 快速短代码检测平台 powered by 智谱清言")
    
    # 初始化会话状态
    if "software_engineer_defect_detection_messages" not in st.session_state:
        st.session_state["software_engineer_defect_detection_messages"] = []
    
    if "uploaded_files" not in st.session_state:
        st.session_state["uploaded_files"] = []

    # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    # 显示历史消息
    with message_placeholder.container():
        for message in st.session_state["software_engineer_defect_detection_messages"]:
            if "file_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (来自文件: {message['file_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])

    # 创建一个固定在底部的输入模块
    with st.container():
        st.write("### 上传代码文件和提问")
        uploaded_files = st.file_uploader("请上传代码文件", type=("py", "cpp", "java", "c", "go", "js", "ts", "html", "css", "scss"), accept_multiple_files=True)
        

    if uploaded_files:
        # 仅对新上传的文件进行处理
        new_files = [file for file in uploaded_files if file.name not in st.session_state["uploaded_files"]]
        
        for file in new_files:
            code = file.read().decode()
            prompt = f"""请检测出代码文件中的代码缺陷，并给出详细的解释。并返回出总共的缺陷数和缺陷类型。并评估代码的质量。同时在针对每一块缺陷代码，给出代码在文件中的位置，和缺陷代码和修复代码以及修复原因。\n\n代码文件名：{file.name}\n\n这是代码文件:\n\n<code>{code}\n\n</code>\n\n"""

            client = ZhipuAI(api_key=openai_api_key)
            response = client.chat.completions.create(
                model="glm-4-plus",  
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            msg = response.choices[0].message.content

            # 更新显示区以显示新消息
            with message_placeholder.container():
                for message in st.session_state["software_engineer_defect_detection_messages"]:
                    if "file_name" in message:
                        st.chat_message(message["role"]).write(f"{message['content']} (来自文件: {message['file_name']})")
                    else:
                        st.chat_message(message["role"]).write(message["content"])
            
                typing_placeholder = st.empty()
                full_msg = ""
                for char in msg:
                    full_msg += char
                    typing_placeholder.chat_message("assistant").write(full_msg)
                    time.sleep(0.05)
                    
                typing_placeholder.chat_message("assistant").write(msg)
                st.session_state["software_engineer_defect_detection_messages"].append({"role": "assistant", "content": msg, "file_name": file.name})

                # 记录已上传的文件
                st.session_state["uploaded_files"].append(file.name)

                # 生成 Markdown 文件内容
                markdown_content = f"# 代码缺陷检测报告\n\n## 文件名: {file.name}\n\n{msg}"

                # 提供下载按钮
                st.download_button(
                    label="下载报告",
                    data=markdown_content,
                    file_name=f"{file.name}_defect_report.md",
                    mime="text/markdown"
                )
                






# 下载 GitHub 项目函数
def download_github_repo(github_url, temp_dir):
    try:
        repo_name = github_url.split('/')[-1]
        repo_dir = os.path.join(temp_dir, repo_name)

        # 克隆 GitHub 仓库到临时目录
        git.Repo.clone_from(github_url, repo_dir)
        return repo_dir
    except Exception as e:
        st.error(f"无法下载项目: {str(e)}")
        return None

async def SoftwareProjectEvaluation():
    st.title("🔎 LLMSDH: 软件缺陷检测平台")
    st.caption("🚀 A Streamlit LLMSDH: 软件缺陷检测平台 powered by 智谱清言")

    # 初始化会话状态
    if "software_project_evaluation_messages" not in st.session_state:
        st.session_state["software_project_evaluation_messages"] = []
    
    if "uploaded_project" not in st.session_state:
        st.session_state["uploaded_project"] = []

    if "github_urls" not in st.session_state:
        st.session_state["github_urls"] = []
        
    # 创建一个固定在顶部的消息显示区域
    message_placeholder = st.empty()

    # 显示历史消息
    with message_placeholder.container():
        for message in st.session_state["software_project_evaluation_messages"]:
            if "project_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (来自项目: {message['project_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])

    # GitHub 链接输入框
    github_url = st.text_input("输入 GitHub 项目链接")

    # 上传文件或通过 GitHub 下载项目
    uploaded_project = st.file_uploader("或者上传项目文件", type=("zip", "tar", "tar.gz", "tar.bz2"), accept_multiple_files=True)
    
    # 检查 GitHub 链接是否为新的
    if github_url and github_url not in st.session_state["github_urls"]:
        st.session_state["github_urls"].append(github_url)  # 记录新的 GitHub 链接
        
        # 下载 GitHub 项目
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_dir = download_github_repo(github_url, temp_dir)
            if repo_dir:
                await  analyze_project_async(repo_dir, message_placeholder, get_repo_name(github_url))

    if uploaded_project:
        # 仅对新上传的项目进行处理
        new_projects = [project for project in uploaded_project if project.name not in st.session_state["uploaded_project"]]
        
        for project in new_projects:
            with tempfile.TemporaryDirectory() as temp_dir:
                if project.name.endswith('.zip'):
                    with zipfile.ZipFile(project, 'r') as zip_ref:
                        zip_ref.extractall(temp_dir)
                elif project.name.endswith(('.tar', '.tar.gz', '.tar.bz2')):
                    with tarfile.open(project, 'r') as tar_ref:
                        tar_ref.extractall(temp_dir)
                await analyze_project_async(temp_dir, message_placeholder, project.name)

# 处理项目的代码文件并评测
def analyze_project(project_dir, message_placeholder, name):
    # 识别代码文件
    code_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(('.py', '.cpp', '.java', '.c', '.go','.rs', '.ipynb')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding=read_file_encoding(file_path), errors='ignore') as f:
                    code_content = f.read()
                file_path = os.path.relpath(os.path.join(root, file), project_dir)
                code_files.append((file, file_path, code_content))
    
    prompts = ["这是一个开发中的软件项目，接下来我会给你项目所有代码文件的名字，路径，内容，请对项目的每个代码文件进行审查。仅仅检测空指针，内存泄漏，并发错误，算术逻辑错误。并给出详细的解释。并评估代码的质量。忽略无关的上下文信息。结合项目代码进行缺陷分析\n\n"]
    
    for file_name, file_path, code_content in code_files:
        prompt = f"""这是代码文件的名字 {file_name} ，代码文件的路径是 {file_path}。结合其他代码文件，进行缺陷分析。代码内容如下：\n\n<code>{code_content}\n\n</code> 仅仅检测空指针，内存泄漏，并发错误，算术逻辑错误。并给出详细的解释。找出代码文件的缺陷。对每个缺陷，给出修复措施和错误原因，忽略无关的上下文信息。对每个缺陷进行代码上下文的定位，并给出修复后的代码。。\n\n"""
        prompts .append(prompt)

    prompts.append("请总结项目的优缺点，对每个文件中的缺陷进行修复。并给出详细的解释，以及修复代码。")
    
   
    msgs = ""
    client = ZhipuAI(api_key=openai_api_key)
    messages = []
    for prompt in prompts:
       
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
        model="glm-4-flash",  
        messages=messages,
    )
        message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": message})
        print(message)
        msgs += message + "\n\n"
    

    prompt = "请评估项目的代码质量，给出项目总结。"
    response = client.chat.completions.create(
        model="glm-4-flash",  
        messages=messages,
    )
    

    msg = response.choices[0].message.content

    msgs += msg + "\n\n"
    
    with message_placeholder.container():
                    for message in st.session_state["software_project_evaluation_messages"]:
                        if "project_name" in message:
                            st.chat_message(message["role"]).write(f"{message['content']} (来自项目: {message['project_name']})")
                        else:
                            st.chat_message(message["role"]).write(message["content"])
                
                    typing_placeholder = st.empty()
                    full_msg = ""
                    for char in msg:
                        full_msg += char
                        typing_placeholder.chat_message("assistant").write(full_msg)
                        time.sleep(0.05)
                        
                    typing_placeholder.chat_message("assistant").write(msg)
                    st.session_state["software_project_evaluation_messages"].append({"role": "assistant", "content": msg, "project_name":name})

                    # 记录已上传的项目
                    st.session_state["uploaded_project"].append(name)

                    # 生成 Markdown 文件内容
                    markdown_content = f"# 项目评估报告\n\n## 项目名: {name}\n\n{msgs}"

                    # 提供下载按钮
                    st.download_button(
                        label="下载报告",
                        data=markdown_content,
                        file_name=f"{name}_project_report.md",
                        mime="text/markdown"
                    )


import asyncio
import aiohttp
from zhipuai import ZhipuAI



async def analyze_project_async(project_dir, message_placeholder, name):
    from zp import process_chunked_prompts, fetch_response
    # 识别代码文件（保持不变）
    code_files = []
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(('.py', '.cpp', '.java', '.c', '.go', '.rs', '.ipynb')):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding=read_file_encoding(file_path), errors='ignore') as f:
                    code_content = f.read()
                file_path = os.path.relpath(os.path.join(root, file), project_dir)
                code_files.append((file, file_path, code_content))

    
    prompts = []
    for file_name, file_path, code_content in code_files:
        prompt = f"""这是代码文件的名字 {file_name} ，代码文件的路径是 {file_path}，结合代码文件进行缺陷分析。代码内容如下：\n\n<code>{code_content}\n\n</code> 仅仅检测空指针，内存泄漏，并发错误，算术逻辑错误。并给出详细的解释。找出代码文件的缺陷。对每个缺陷，给出修复措施和错误原因，忽略无关的上下文信息。对每个缺陷进行代码上下文的定位，并给出修复后的代码。返回的格式是"这是针对xxx代码文件，的缺陷检测报告。"\n\n"""
        prompts.append(prompt)

    
    
    msgs = ""
    client = ZhipuAI(api_key=openai_api_key)
    
    
    # 等待所有任务完成
    responses, messages = await process_chunked_prompts(prompts=prompts, api_key=openai_api_key)
    
    # 处理每个响应
    for message in responses:
        msgs += message + "\n\n"

    # 最后总结项目的代码质量
   
    final_response= "针对项目{}的缺陷检测成功！！！".format(name)

    # 显示评估结果
    with message_placeholder.container():
        for message in st.session_state["software_project_evaluation_messages"]:
            if "project_name" in message:
                st.chat_message(message["role"]).write(f"{message['content']} (来自项目: {message['project_name']})")
            else:
                st.chat_message(message["role"]).write(message["content"])
        
        typing_placeholder = st.empty()
        full_msg = ""
        for char in final_response:
            full_msg += char
            typing_placeholder.chat_message("assistant").write(full_msg)
            await asyncio.sleep(0.05)  # 异步等待
        typing_placeholder.chat_message("assistant").write(final_response)
        st.session_state["software_project_evaluation_messages"].append({"role": "assistant", "content": final_response, "project_name": name})

        # 记录已上传的项目
        st.session_state["uploaded_project"].append(name)

        # 生成 Markdown 文件内容
        markdown_content = f"# 项目评估报告\n\n## 项目名: {name}\n\n{msgs}"

        # 提供下载按钮
        st.download_button(
            label="下载报告",
            data=markdown_content,
            file_name=f"{name}_project_report.md",
            mime="text/markdown"
        )






def main():  
    if "current_page" not in st.session_state:  
        st.session_state.current_page = "home"  
  
    st.sidebar.title("LLMSDH: 大模型助力软件开发")  
    if st.sidebar.button("💬 LLMSDH: 软件原型开发平台"):  
        st.session_state.current_page = "chatbot"  
    if st.sidebar.button("🦜🔗 LLMSDH: 软件系统介绍开发平台"):  
        st.session_state.current_page = "codegeex"  
    if st.sidebar.button("📝 LLMSDH: 快速短代码检测平台"):  
        st.session_state.current_page = "Software Engineer Defect Detection"  
    
    if st.sidebar.button("🔎LLMSDH: 软件缺陷检测平台"):
        st.session_state.current_page = "Software Project Evaluation"  
        


    if st.session_state.current_page == "chatbot":  
        chatbot_page()  
    elif st.session_state.current_page == "codegeex":  
        CodeGeeXIntrepreting()  
    elif st.session_state.current_page == "Software Engineer Defect Detection":  
        SoftwareEngineerDefectDetection()  
    elif st.session_state.current_page == "Software Project Evaluation":  
        asyncio.run(SoftwareProjectEvaluation())  
        
  
if __name__ == "__main__":  
    main()
