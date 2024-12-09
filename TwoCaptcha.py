from twocaptcha import TwoCaptcha

#solver = TwoCaptcha('3f4a45268126b679b270f3e31f2b604a')

config = {
            'server':           '2captcha.com',
            'apiKey':           '3f4a45268126b679b270f3e31f2b604a',
            'softId':            123,
            'callback':         'https://your.site/result-receiver',
            'defaultTimeout':    120,
            'recaptchaTimeout':  600,
            'pollingInterval':   10,
            'extendedResponse':  False
        }
solver = TwoCaptcha(**config)