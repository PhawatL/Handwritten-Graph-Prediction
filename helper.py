e = 1e-7
class make_fuc:
    
    def __init__(self,w,degree) -> None:
        self.w = w
        self.degree = degree
    def fuc(self,x,*,w= None):
        ans = 0
        degree = self.degree
        for i in range(len(self.w)):
            ans +=self.w[i]*(x+e)**(degree)
            degree -= 1
        return ans
    def __call__(self,x):
        return self.fuc(x)
    
    def __repr__(self) -> str:
        s = ''
        degree = self.degree
        for i in range(len(self.w)):
            s += ' +' if self.w[i] >0 else ' '
            if degree == 0:
                s += f'{round(self.w[i],6)}'
            else:
                s += f'{round(self.w[i],6)}x^{degree}'
            degree -=1
        
        
        return s
    
    
class StdoutRedirector():
    def __init__(self,widget):
        self.widget = widget

    def write(self,string):
        self.widget.insert("end",string)
        self.widget.see("end")
        
    def flush(self):
        pass
    
def diff_fuc(f,g,*,n=20):
    
    diff = 0
    for i in range(n):
        diff = abs(f(i)-g(i))
    return diff/n

if __name__ == '__main__':
    print("don't run this file")
