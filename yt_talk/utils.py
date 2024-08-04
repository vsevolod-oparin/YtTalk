def time_format(seconds):
    seconds = int(float(seconds))
    minutes = seconds // 60
    hours = minutes // 60

    seconds = seconds % 60
    minutes = minutes % 60

    if hours > 0:
        return f'{hours}:{minutes:02d}:{seconds:02d}'
    if minutes > 0:
        return f'{minutes}:{seconds:02d}'
    return f'{seconds}'


def main():
    print(time_format(17.4))
    print(time_format(127.4))
    print(time_format(3607.4))


if __name__ == '__main__':
    main()
