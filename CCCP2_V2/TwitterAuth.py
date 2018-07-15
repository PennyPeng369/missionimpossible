'''
Team: Team 22
City: Melbourne
Name: Yanjun Peng (906571)
       Na Chang (858604)
       Zepeng Dan (933678)
       Junhan Liu (878637)
       Peishan Li (905508)
'''

class TwitterAuth:
    # Structures shown below
    # Name,CustomerKey,
    # consumerSecret,
    # accessToken,
    # accessTokenSecret

    def __init__(self, cKey, cSec, aToken, aSec):
        self.cKey = cKey
        self.cSec = cSec
        self.aToken = aToken
        self.aSec = aSec


userAuth = {

    'Liu1': TwitterAuth(
                        "wzHVq78rberaGlO09x93t4pPL",
                        "B8baMfgvInPpkq3bnFjV9sx9oFdqto41ybJjirw44VdV4iEf6b",
                        "986421463090511872-Zs3n0RayLuod1y4goV5XeSXqLfUew5E",
                        "bkCnuxxqLf6ZuQtUzd8AkCYJER55DOP93QemoagX9h2DE"
                        ),

    "Liu2": TwitterAuth(
                        "x4ugrQcyanEDaQK1vZShF7GtJ",
                        "oIEC1XNanmIML02uGojooaEGaiewrrGYFZy3GPUQx2jg6oYbzD",
                        "954298550-xYgWgDSeM4rlIPP00mAMQKFYTfARdNjje1aqmsxD",
                        "z06ebZME6TZTd6TL6YigIByuripH8SXC5GMYSY8rUzceE"
                        ),

    "Liu3": TwitterAuth(
                        "WTViYMJPhbWqmvKA7E8qw9ai5",
                        "hnJ3X5ymXuVti1Z1FgUE4nkkGpOEJKBJToE5Za19HP3lvv0Kcr",
                        "954298550-59xIdMHaylP9y8W7OFuJ3V7e4YJpXn9LE8hS6KAQ",
                        "K0IDmkIRyLzXfwHuj4IZOMAXnBR7IvNBUu5e1Fnevlphq"
                        ),

    "Liu4": TwitterAuth(
                        "jOE7GEGdob6jcjlTBz6pxWRlM",
                        "AN5o27SN6Od6AkTGxWermCeTzPjSUlBFHJd2mmz9K1OETYNaxJ",
                        "986421463090511872-GXFk5b4EsEcaccwenx6YbEYFftlkSyV",
                        "CAH2V8QHmLVePYyUMz33mTjPwy4DFw0MlX9L3k9zBBVUb"
                        ),

    "Liu5": TwitterAuth(
                        "Fex1yo4NMRl49Xy7XY2WPuuwV",
                        "khbr8Dqh6w2tDJDaB7R1eMJ4tDptiYfx6fRRW81oNSKEx8gE89",
                        "986421463090511872-Us9uESuMhRSWPiGggmVRCo0WF54Rmbk",
                        "NRGHY0i3QVjNg32tuN4E43kkP5GXO9pZKwDUlq55MOmx3"
                        ),

    "Dan1": TwitterAuth("D4epiQLjWEDKJ1IJBslijXxso",
                        "Hw6zjd0VN16IGDNXYiF3ZnPsJtKn7BRjwduUCJ4HGwbeoYSPjB",
                        "856808494476951552-V4JnjPE8qbu6Qi7jSTYVCksS0Ya8H4o",
                        "CkQl5kFr4NNcZK7CchPaWskw8rhR1KXiWmYWKPQE3zK1s"
                        ),

    "Stalker": TwitterAuth("O4CwmREKIHf2F5mzxFYob7VQ2",
                           "OXwORqnESbySvMv3Lq13nsTT7gsAPG8dGGgZN7JFkLtXI9VQlT",
                           "856808494476951552-f9NK4Yz2bK6f5HXZ37xZhhbIa0HghoM",
                           "ik7n3ws1xd0cOfEiC2VLeLwuf8SeDpHOtR2H2GUKl6lsd")
}
