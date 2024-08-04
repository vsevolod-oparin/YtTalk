from dataclasses import dataclass


@dataclass
class YtData:
    video_id: str
    watch_link: str
    embed_link: str

    @staticmethod
    def create(link):
        idd = YtData._form_idd(link)
        if idd is None:
            return None
        return YtData(
            video_id=idd,
            watch_link=f'https://www.youtube.com/watch?v={idd}',
            embed_link=f'https://www.youtube.com/embed/{idd}',
        )

    @staticmethod
    def _form_idd(link):
        if 'youtu.be/' in link:
            parts = link.strip().split('youtu.be/')
            if len(parts) <= 1:
                return None
            return parts[1].split('?')[0]
        elif '/embed/' in link:
            parts = link.strip().split('/embed/')
            if len(parts) != 2:
                return None
            return parts[1]
        elif 'watch?' in link:
            parts = link.split('watch?')
            if len(parts) == 1:
                return None
            arg_list = parts[1].split('&')
            for arg in arg_list:
                if arg.startswith('v='):
                    return arg[2:]
            return None
        return None


def main():
    print(YtData.create('https://www.youtube.com/watch?v=gD5IA51OdpM&t=0s'))
    print(YtData.create('https://youtu.be/hplbkvc0ejo?si=DexwR5coGZ-RLExm&t=1'))
    print(YtData.create('https://www.youtube.com/watch?v=hplbkvc0ejo'))
    print(YtData.create('https://www.youtube.com/embed/hplbkvc0ejo'))


if __name__ == '__main__':
    main()
