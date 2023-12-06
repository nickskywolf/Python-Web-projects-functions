from mongoengine import connect
from insert_data import Authors, Quotes
import re


def find_by_author(author_name: str):
    author = Authors.objects(fullname=author_name.strip().title()).first()
    quotes = [document.quote for document in Quotes.objects(author=author)]
    return quotes


def find_by_tag(tag_name: str):
    quotes = Quotes.objects(tags__in=[tag_name])
    return [quote.quote for quote in quotes]


def find_by_tags(tags: str):
    tags = [tag.strip().lower() for tag in tags.split(',')]
    quotes_set = Quotes.objects(tags__in=tags)
    return [quote.quote for quote in quotes_set]


if __name__ == '__main__':

    connect(db='hw8',
            host='mongodb+srv://mihanch:****@cluster0.xo49jrs.mongodb.net/')
    while True:
        print('Please enter your command in the following format: command: value')
        user_input = input()
        if re.match('[a-zA-Z]+:\s?[a-zA-z]+', user_input.strip().lower()):
            user_input = user_input.strip().split(':')
            if user_input[0].strip().lower() == 'name':
                for quote in find_by_author(user_input[1]):
                    print(quote)
            elif user_input[0].strip().lower() == 'tag':
                for quote in find_by_tag(user_input[1]):
                    print(quote)
            elif user_input[0].strip().lower() == 'tags':
                for quote in find_by_tags(user_input[1]):
                    print(quote)
            else:
                print('Unknown command')
        elif user_input == 'exit':
            exit()
        else:
            print('Unknown command or incorrect format')