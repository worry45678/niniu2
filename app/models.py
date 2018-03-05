from . import db
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manger
from datetime import datetime
import math, random, json, itertools

PUKE = ['fangp01', 'fangp02', 'fangp03', 'fangp04', 'fangp05', 'fangp06', 'fangp07', 'fangp08', 'fangp09', 'fangp10',
'fangp11', 'fangp12', 'fangp13', 'hongt01', 'hongt02', 'hongt03', 'hongt04', 'hongt05', 'hongt06', 'hongt07', 'hongt08',
'hongt09', 'hongt10', 'hongt11', 'hongt12', 'hongt13', 'heit01', 'heit02', 'heit03', 'heit04', 'heit05', 'heit06', 'heit07',
'heit08', 'heit09', 'heit10', 'heit11', 'heit12', 'heit13', 'meih01', 'meih02', 'meih03', 'meih04', 'meih05', 'meih06',
'meih07', 'meih08', 'meih09', 'meih10', 'meih11', 'meih12', 'meih13']

HUASE_NUMBER= {'heit':0.4,'hongt':0.3,'meih':0.2,'fangp':0.1}

BEI_LV = {0:1,1:1,2:1,3:1,4:1,5:1,6:1,7:1,8:2,9:2,10:3}

def calcniuniu(pai):
    l2 = [int(i[-2:]) if int(i[-2:])<10 else 10 for i in pai]
    diansu = 0
    for i in itertools.combinations(l2,3):
        if sum(i)%10==0:
            diansu=(sum(l2)-sum(i))%10
            if diansu == 0:
                diansu = 10
    l3 = {int(i[-2:])+HUASE_NUMBER[i[0:-2]]:i for i in pai}
    return diansu,l3[max(l3.keys())],max(l3.keys())

def compare(pai1,pai2):
    """
    参数1，庄的牌，参数2，玩家的牌,庄小，返回+，庄大，返回-
    """
    if pai1[0]+pai1[2]/100 < pai2[0]+pai2[2]/100:
        return BEI_LV[pai2[0]]
    else:
        return -1 * BEI_LV[pai1[0]]

def calcmark(pai):
    paixu = json.loads(pai.paixu)
    if pai.zhuang == 1:
        zhuang = int(pai.user1_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[0]),calcniuniu(paixu[4]))
        pai.user1_mark = -pai.user2_mark-pai.user3_mark-pai.user4_mark-pai.user5_mark
    elif pai.zhuang == 2:
        zhuang = int(pai.user2_xiazhu)
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[0]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[1]),calcniuniu(paixu[4]))
        pai.user2_mark = -pai.user1_mark-pai.user3_mark-pai.user4_mark-pai.user5_mark
    elif pai.zhuang == 3:
        zhuang = int(pai.user3_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[1]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[0]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[3]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[2]),calcniuniu(paixu[4]))
        pai.user3_mark = -pai.user1_mark-pai.user2_mark-pai.user4_mark-pai.user5_mark
        print(type(pai.user2_mark),pai.user2_mark)
    elif pai.zhuang == 4:
        zhuang = int(pai.user4_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[2]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[0]))
        pai.user5_mark = int(pai.user5_xiazhu) * zhuang * compare(calcniuniu(paixu[3]),calcniuniu(paixu[4]))
        pai.user4_mark = -pai.user1_mark-pai.user2_mark-pai.user3_mark-pai.user5_mark
    elif pai.zhuang == 5:
        zhuang = int(pai.user5_xiazhu)
        pai.user2_mark = int(pai.user2_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[1]))
        pai.user3_mark = int(pai.user3_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[2]))
        pai.user4_mark = int(pai.user4_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[3]))
        pai.user1_mark = int(pai.user1_xiazhu) * zhuang * compare(calcniuniu(paixu[4]),calcniuniu(paixu[0]))
        pai.user5_mark = -pai.user1_mark-pai.user2_mark-pai.user3_mark-pai.user4_mark
    return pai

class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(8))
    password_hash = db.Column('password', db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.ID'))
    money = db.Column('money', db.Integer)
    photo = db.Column('photo', db.String(128))
    openid = db.Column('openid', db.String(20))
    room1s = db.relationship('Room', backref='user1', lazy='dynamic', primaryjoin='(User.id==Room.user1_id)')
    room2s = db.relationship('Room', backref='user2', lazy='dynamic', primaryjoin='(User.id==Room.user2_id)')
    room3s = db.relationship('Room', backref='user3', lazy='dynamic', primaryjoin='(User.id==Room.user3_id)')
    room4s = db.relationship('Room', backref='user4', lazy='dynamic', primaryjoin='(User.id==Room.user4_id)')
    room5s = db.relationship('Room', backref='user5', lazy='dynamic', primaryjoin='(User.id==Room.user5_id)')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role_id is None: # 如果名称为admin，则设为管理员
            if self.name == 'admin':
                self.role_id = Role.query.filter_by(permissions=0xff).first().id
            if self.role_id is None:
                self.role_id = Role.query.filter_by(default=True).first().id
    def __repr__(self):
        return '''{"id":"%d","name":"%s"}''' %(self.id,self.name)
    
    def can(self, permissions): # 判断角色是否包含所有请求权限，包含则返回True
        return self.role_id is not None and (self.rolename.permissions & permissions) == permissions
    
    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return  check_password_hash(self.password_hash, password)

    def rooms(self):
        return self.room1s.all() + self.room2s.all() + self.room3s.all() + self.room4s.all() +self.room5s.all()


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False
    
    def is_administrator(self):
        return False

class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Name', db.String(16))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column('Permission', db.Integer)
    users = db.relationship('User', backref='rolename', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW | Permission.COMMENT | Permission.WRITE_ARTICLES | Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class Permission:
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Room(db.Model):
    __tablename__ = 'room'
    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    createtime = db.Column(db.DateTime(), default=datetime.utcnow)
    rank = db.Column('rank', db.Integer, default=0)
    user1_id = db.Column(db.Integer, db.ForeignKey('User.ID'))
    user2_id = db.Column(db.Integer, db.ForeignKey('User.ID'))
    user3_id = db.Column(db.Integer, db.ForeignKey('User.ID'))
    user4_id = db.Column(db.Integer, db.ForeignKey('User.ID'))
    user5_id = db.Column(db.Integer, db.ForeignKey('User.ID'))
    end = db.Column('end', db.Boolean, default=False)
    paijus = db.relationship('Paiju', backref='roomname', lazy='dynamic')
    status = db.Column('status',db.Text, default=0)

    def __init__(self,**kwargs):
        super(Room, self).__init__(**kwargs)
        self.id = random.randint(100000,1000000)

    def userpos(self, user):
        if self.user1_id == user.id:
            return 1
        elif user.id == self.user2_id:
            return 2
        elif user.id == self.user3_id:
            return 3
        elif user.id == self.user4_id:
            return 4
        elif user.id == self.user5_id:
            return 5
        else:
            return 0

    def count(self):
        if self.user2_id is None:
            return 1
        elif self.user3_id is None:
            return 2
        elif self.user4_id is None:
            return 3
        elif self.user5_id is None:
            return 4
        else:
            return 5
    
    def __repr__(self):
        user1 = self.user1.name if self.user1 else None
        user2 = self.user2.name if self.user2 else None
        user3 = self.user3.name if self.user3 else None
        user4 = self.user4.name if self.user4 else None
        user5 = self.user5.name if self.user5 else None
        return '''{"id": "%s","createtime":"%s","confirm":"%s","user1":"%s","user2":"%s","user3":"%s","user4":"%s","user5":"%s","end":"%s"}''' \
               %(self.id,self.createtime,self.confirm, user1, user2, user3, user4, user5, self.end) 

    def join(self, player):
        if self.user2_id == None :
            self.user2_id = player.id
            return 2
        elif self.user3_id == None:
            self.user3_id = player.id
            return 3
        elif self.user4_id == None:
            self.user4_id = player.id
            return 4
        elif self.user5_id ==None:
            self.user5_id = player.id
            return 5
        else:
            return 'no'

    def getStatus(self,current_user):
        user1 = self.user1.name if self.user1 else None
        user2 = self.user2.name if self.user2 else None
        user3 = self.user3.name if self.user3 else None
        user4 = self.user4.name if self.user4 else None
        user5 = self.user5.name if self.user5 else None

        return '''{"id": %d,"createtime":"%s","users":["%s","%s","%s","%s","%s"],"count":%d,"roomstatus":"%s","seat":%d,"rank":%d}''' \
                %(self.id,self.createtime, user1, user2, user3, user4, user5, self.count(), self.status, self.userpos(current_user), self.rank) 

class Paiju(db.Model):
    __table__name = 'paiju'
    id = db.Column('ID', db.Integer, primary_key=True, autoincrement=True)
    room_id = db.Column(db.Integer, db.ForeignKey('room.ID'))
    paixu = db.Column('paixu', db.String(700))
    createtime = db.Column(db.DateTime(), default=datetime.utcnow)
    ready = db.Column('ready', db.Integer, default=0)
    zhuang = db.Column('zhuang', db.Integer, default=0)
    done = db.Column('done', db.Integer, default=0)
    finish = db.Column('finish', db.Boolean, default=False)
    user1_xiazhu = db.Column(db.Integer, default=0)
    user2_xiazhu = db.Column(db.Integer, default=0)
    user3_xiazhu = db.Column(db.Integer, default=0)
    user4_xiazhu = db.Column(db.Integer, default=0)
    user5_xiazhu = db.Column(db.Integer, default=0)
    xiazhudone = db.Column('xiazhudone', db.Integer, default=0)
    user1_mark = db.Column(db.Integer, default=0)
    user2_mark = db.Column(db.Integer, default=0)
    user3_mark = db.Column(db.Integer, default=0)
    user4_mark = db.Column(db.Integer, default=0)
    user5_mark = db.Column(db.Integer, default=0)
    status = db.Column('status', db.Text, default='ready')

    @staticmethod
    def generate_paiju(room):
        new_puke = PUKE.copy()
        for i in range(20):
            random.shuffle(new_puke)
            r = [new_puke[0:5],new_puke[5:10],new_puke[10:15],new_puke[15:20],new_puke[20:25]]
            new_paiju = Paiju(room_id=room, paixu=json.dumps(r))
            db.session.add(new_paiju)
            db.session.commit()
    
    def choicezhuang(self):
        l = [self.user1_xiazhu,self.user2_xiazhu,self.user3_xiazhu,self.user4_xiazhu,self.user5_mark]
        l2 = [2**i for i in range(5) if l[i]==max(l)]
        self.zhuang = math.log(random.choice(l2))/math.log(2) + 1

    def xiazhu(self,pos,zhu):
        if pos == 1:
            self.user1_xiazhu = zhu
        elif pos == 2:
            self.user2_xiazhu = zhu
        elif pos == 3:
            self.user3_xiazhu = zhu
        elif pos ==4:
            self.user4_xiazhu = zhu
        else:
            self.user5_xiazhu = zhu
        db.session.add(self)
        db.session.commit()
    
    def checkxiazhu(self, room):
        if room.user1_id !=0 and self.user1_xiazhu == 0:
            return False
        elif room.user2_id !=0 and self.user2_xiazhu == 0:
            return False
        elif room.user3_id !=0 and self.user3_xiazhu == 0:
            return False
        elif room.user4_id !=0 and self.user4_xiazhu == 0:
            return False
        elif room.user5_id !=0 and self.user5_xiazhu == 0:
            return False
        else:
            return True
    
    def marks(self):
        #return '''{"id":%d,"marks":["%d","%d","%d","%d","%d"]}'''\
        #        %(self.id, self.user1_mark, self.user2_mark, self.user3_mark, self.user4_mark, self.user5_mark)
        return [self.user1_mark, self.user2_mark, self.user3_mark, self.user4_mark, self.user5_mark]

    def __repr__(self):
        return '''{"user1":%d,"user2":%d,"user3":%d,"user4":%d}''' \
                %(self.user1_mark,self.user2_mark,self.user3_mark,self.user4_mark)
    
    def marks2(self):
        return {'user1':self.user1_mark,'user2':self.user2_mark,'user3':self.user3_mark,'user4':self.user4_mark}

login_manger.anonymous_user = AnonymousUser


@login_manger.user_loader
def load_user(user_id):
    """
    加载用户，存在则返回用户对象，不存在则返回None。
    """
    return User.query.get(int(user_id))