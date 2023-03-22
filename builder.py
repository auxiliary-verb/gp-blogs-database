#!/usr/bin/python3
import json
import glob
import os
import shutil

outFolder = './out'
articlesFolder = './articles'
archivesFolder = './archives'
masterFolder = './master'
searchFile = '*.json'
listFile = 'list.json'

def main():
    if not setting():
        print('Setting Error.')
        return

    # Get file list
    files = glob.glob(os.path.join(articlesFolder, searchFile))

    builder = list_builder()
    for file in files:
        # Get json info
        name, title, body, createdDate, thumbnail, tags =get_fileinfo(file)

        # Copy to out folder
        if createdDate != "":
            create_outfile(file)

        # Create archive file
        create_md(file, body)

        builder.append(name,title,createdDate, thumbnail,tags)
    # Create file list
    builder.build()

    # Get file list
    files = glob.glob(os.path.join(masterFolder, searchFile))
    for file in files:
        # Copy to out folder
        create_outfile(file)


def setting():
    # Folder check
    if(not os.path.isdir(articlesFolder)):
        return False
    if(not os.path.isdir(archivesFolder)):
        os.mkdir(archivesFolder)

    # out folder clear
    if(os.path.isdir(outFolder)):
        shutil.rmtree(outFolder)
    os.mkdir(outFolder)
    return True

def create_outfile(file):
    filename = os.path.basename(file)
    outPath = os.path.join(outFolder, filename)

    # Copy to out folder
    shutil.copyfile(file, outPath)

def create_md(file, body):
    filename = os.path.basename(file)

    # Create archive file
    filebase = os.path.splitext(filename)[0]
    archivePath = os.path.join(archivesFolder, filebase + '.md')
    with open(archivePath, 'w') as fs: 
        fs.write(body)

def get_fileinfo(file):
    name = os.path.splitext(file)[0]
    with open(file, 'r') as fs: 
        fsJson = json.load(fs)
        body = str( fsJson['body'] )
        title = str( fsJson['title'] )
        thumbnail = str( fsJson['thumbnail'] )
        createdDate = ""
        if 'createdDate' in fsJson:
            createdDate = str( fsJson['createdDate'] )
        tags = fsJson['tags']
    return [
        name, 
        title, 
        body, 
        createdDate,
        thumbnail,
        tags,
    ]

class list_builder:
    def __init__(self):
        self.file_list = []
    def append(self, name, title, createdDate, thumbnail, tags):
        if createdDate != "":
            self.file_list.append({
                "name": name, 
                "title": title, 
                "createdDate": createdDate,
                "thumbnail": thumbnail,
                "tags": tags,
            })

    def build(self):
        body = json.dumps({'files': self.file_list})
        file =  os.path.join(outFolder, listFile)
        with open(file, 'w') as fs: 
            fs.write(body)

if __name__ == "__main__":
    main()
  