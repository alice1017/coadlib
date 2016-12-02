#!/usr/bin/env python
# coding: utf-8

import sys
import codecs
import chardet
import logging
import platform

PLATFORM = platform.system()

if PLATFORM == "Windows":
    ENCODING = "shift_jis"

else:
    ENCODING = "utf-8"


class Application(object):
    """The API class of creating an application."""


    def __init__(self, name, desc, version,
                    padding, margin, encoding=ENCODING):
        """Initialize application

        args:
        * name - The application name, used by usage msg.
        * desc - The description of application, used by usage msg.
        * version - The application version, used by usage msg.
        * padding - The width from left side of terminal window to the string area.
        * margin - The height from top side of terminal window to the string area.
        * encoding - The application encoding. 
        """

        self.name = name
        self.desc = desc
        self.version = version
        self.padding = u" "*padding
        self.margin = u"\n"*margin
        self.encoding = encoding

        stream = codecs.getwriter(self.encoding)
        log_stream = stream(sys.stderr)

        self.logger = self.getlogger(stream=log_stream)
        self.stdout = _stream(sys.stdout)

        if PLATFORM == "Windows":
            self.stdin = codecs.getreader(self.encoding)(sys.stdin)
        
        else:
            self.stdin = sys.stdin

    def getlogger(self, stream=sys.stderr, level=logging.DEBUG):

        logger = logging.getLogger(self.name)

        handler = logging.StreamHandler(stream)
        handler.setLevel(level)

        logger.setLevel(level)
        logger.addHandler(handler)

        return logger

    def pp(self, msg, margin=False):

        if isinstance(msg, str):
            try:
                msg = unicode(msg, self.encoding)
            except:
                msg = msg.decode(chardet.detect(msg)["encoding"], "")
        
        if "\n" in msg:

            contents = []

            for line in msg.split("\n"):
                if line == "":
                    contents.append(self.padding)

                else:
                    contents.append(self.padding + line)
            
            result_msg = "\n".join(contents)

        else:
            result_msg = self.padding + msg

        if margin:
            return self.margin + result_msg

        else:
            return result_msg

    def print_usage(self):

        msg = u"{0} version: {1}\n\n{2}\n\n".format(
                    self.name, self.version, self.desc)
        self.logger.info(self.pp(msg, margin=True))

    def exit(self, exit_code):

        self.stdout.write(self.pp(u"\nEnterを押すと終了します"))
        self.stdin.readline()
        sys.exit(exit_code)

    def __repr__(self):

        return u"<{0} v{1}>".format(self.name, self.version)

    def __str__(self):

        return self.__repr__()



