from dingtalkchatbot.chatbot import DingtalkChatbot
from weibo import Weibo
import requests


class Push(object):

    def __init__(self, token=None, keyWord=None, sercret=None, weiboRef=None, weiboCookie=None, weiboSCF=None, weixinToken=None):
        self.useDingTalk = False
        self.useWeibo = False
        self.useSCF = False
        self.useWeixin = False
        if token and keyWord:
            self.useDingTalk = True
            self.d = DingtalkChatbot(
                'https://oapi.dingtalk.com/robot/send?access_token=%s' % token, secret=sercret)
            self.keyWord = keyWord
            print(self.keyWord)
            print(token)
        if weiboRef and weiboCookie:
            self.useWeibo = True
            self.weibo = Weibo(weiboRef, weiboCookie)
        if weiboSCF:
            self.useSCF = True
            self.weiboSCF = weiboSCF
        if weixinToken:
            self.useWeixin = True
            self.wxurl = 'https://sc.ftqq.com/%s.send' % weixinToken

    def sendMsg(self, title, msg, is_at_all=False):
        if self.useDingTalk:
            print("dingtalk")
            self.d.send_markdown(title=self.keyWord + title,
                                 text=msg, is_at_all=is_at_all)
        if self.useWeibo:
            self.weibo.send(msg)
        if self.useSCF:
            requests.post(self.weiboSCF, data=msg.encode("utf-8"))
        if self.useWeixin:
            data = {
                'text': title,
                'desp': msg
            }
            requests.post(self.wxurl, data=data)


if __name__ == '__main__':
    import config

    msg = '# 重要通知【人社部：企业不得开除因疫情不能正常上班的员工】人社部24日对外发布通知，明确对新型冠状病毒感染的肺炎患者、疑似病人、密切接触者在其隔离治疗期间或医学观察期间以及因政府实施隔离措施或采取其他紧急措施导致不能提供正常劳动的企业职工，企业应当支付职工在此期间的工作报酬，并不得依据劳动合同法第四十条、四十一条与职工解除劳动合同。在此期间，劳动合同到期的，分别顺延至职工医疗期期满、医学观察期期满、隔离期期满或者政府采取的紧急措施结束。（澎湃新闻）'
    push = Push(config.PushToken, config.PushKeyWord, config.pushSecret,
                config.WeiboRef, config.WeiboCookie, config.WeiboSCFUrl)
    # push.sendMsg("Giao", msg)
    # push = Push(weixinToken=config.WeixinToken)
    push.sendMsg("", msg)
