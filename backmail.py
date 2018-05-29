
#!/usr/bin/env python3

# coding: utf-8

import os

import zipfile

from pathlib import Path

import smtplib

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email import encoders

colours = {"red": "\033[31m", "white": "\033[37m",
           "green": "\033[32m", "yellow": "\033[33m", "blue": "\033[34m"}


class BackArchive:

    def __init__(self) -> None:
        self.__paths = list()

    def get_all_paths(self, root_path: str=os.getcwd()) -> None:
        '''Get all paths in the current directory or a directory informed by the user'''

        for root, subfiles, files in os.walk(root_path):
            for name in files:
                self.__paths.append(os.path.join(root, name))

    def insert_path(self, path: str = "") -> None:
        '''Insert a specific path'''

        self.__paths.append(path)

    def show_all_paths(self) -> None:
        '''Print all paths'''

        if(len(self.__paths)):
            for counter in range(len(self.__paths)):
                print("\n{0}➜{2} {1}{3}{2} {4}\n".format(
                    colours["green"], colours["blue"], colours["white"], counter, self.__paths[counter]))
        else:
            print("\n{0}➜{2} There's no {1}paths{2} to print\n".format(
                colours["green"], colours["red"], colours["white"]))

    def get_specific_path(self, indice: int = 0) -> str:
        '''Get a specific path as from index'''

        if(len(self.__paths)):
            try:
                print("\n{0}➜{2} {1}{3}{2} {4}\n".format(
                    colours["green"], colours["red"], colours["white"], indice, self.__paths[indice]))

                return self.__paths[indice]
            except:
                print("\n{0}➜{2} There's no {1}path{2} or the {1}index{2} is out of range\n".format(
                    colours["green"], colours["red"], colours["white"]))

                return ""

    def get_path_by_type(self, extension: str = "") -> list:
        '''Get a specific path as from format'''

        items = list()

        if(len(self.__paths)):
            if(not extension.startswith(".")):
                extension = "." + extension

            for item in self.__paths:
                if(extension in item):
                    items.append(item)
        else:
            items.append("")

        return items

    def remove_path(self, path_indice: int = 0) -> None:
        '''Remove a specific path as from index'''

        if(len(self.__paths)):
            try:
                self.__paths.remove(path_indice)

                print("\n{0}➜{2} Path {1}removed{2}\n".format(
                    colours["green"], colours["red"], colours["white"]))
            except:
                print("\n{0}➜{2} Can't {1}remove{2} on indice {3}\n".format(
                    colours["green"], colours["red"], colours["white"], path_indice))
        else:
            print("\n{0}➜{2} The {1}path{2} list is empty\n".format(
                colours["green"], colours["red"], colours["white"]))

    def zip_all_files(self):
        '''Zip all files in the path list, using Lzma compression'''

        with zipfile.ZipFile("backmail.zip", "w") as zip_file:
            for path in self.__paths:
                if(os.path.isfile(path)):
                    zip_file.write(path, path.split(
                        "/")[-1], compress_type=zipfile.ZIP_LZMA)
                elif(Path(path).is_dir()):
                    print("\n{0}➜{2} Can't compress the folder: {2}{1}{3}{2}\n".format(
                        colours["green"], colours["red"], colours["white"], path))  # Feature : implement the recursion of folders
                else:
                    print("\n{0}➜{2} Can't be found: {2}{1}{3}{2}\n".format(
                        colours["green"], colours["red"], colours["white"], path))


class BackMail:

    def __init__(self, mail_from: str ="", passwd: str ="", mail_to: str ="", subject: str ="", message: str=""):
        self.__mail_from = mail_from

        self.__passwd = passwd

        self.__mail_to = mail_to

        self.__subject = subject

        self.__message = message

        self.__server = smtplib.SMTP("smtp.gmail.com", 587)

        self.__server.starttls()

        self.__server.login(mail_from, passwd)

        self.__msg = MIMEMultipart()

        self.__msg["From"] = mail_from

        self.__msg["To"] = mail_to

        self.__msg["Subject"] = subject

        self.__msg.attach(MIMEText(message, "plain"))

        self.__message = self.__msg.as_string()

    def add_file(self, name_file: str =""):
        '''Add a file to the e-mail body'''

        cache_file = open(name_file, "rb")

        cache_mime = MIMEBase("application", "octet-stream")

        cache_mime.set_payload((cache_file).read())

        encoders.encode_base64(cache_mime)

        cache_mime.add_header("Content-Disposition",
                              "attachment; filename=" + name_file)

        self.__msg.attach(cache_mime)

        self.__message = self.__msg.as_string()

    def send_mail(self):
        try:
            self.__server.sendmail(
                self.__mail_from, self.__mail_to, self.__message)

            self.__server.quit()
        except:
            print("\nConnection {0}closed{1}, can't send the e-mail\n".format(
                colours["red"], colours["white"]))


if __name__ == "__main__":

    print("\n{0}Back{2}:{1}Mail{2}\n".format(
        colours["red"], colours["blue"], colours["white"]))

    # Menu, e-mail from yahoo and outlook, cryptography, zip folders, gui, deb file ...
