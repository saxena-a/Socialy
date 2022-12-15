    from flask import Flask, render_template,request, url_for, flash, redirect, session
    from firebasecred import config
    import pyrebase
    from friends import getFriends
    import time


    ts = time.time()
    app = Flask(__name__)
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    database = firebase.database()
    app.secret_key = 'secret'
    allUsers = {}
    friendNames = {}

def socialy():
    app = Flask(__name__)

    @app.route("/",methods=('GET','POST'))
    def index():
        try:
            if(request.form.getlist('signin')[0]=='submit'):
                try:
                    user = auth.sign_in_with_email_and_password(request.form.getlist('username')[0],request.form.getlist('password')[0])
                    session['user'] = user['localId']
                    return redirect("/homepage")


                except Exception as e:
                    print(e)
                    return render_template("sign-in.html", alert="yes",message="Cannot sign in. Seems username doesn't exist or password is wrong")

        except:
            pass
        try:
            if(request.form.getlist('signup')[0]=='submit'):
                if(request.form.getlist('password')[0]==request.form.getlist('repeat-password')[0] and len(request.form.getlist('repeat-password')[0])>6):
                    try:
                        #
                        data = {
                            'name':request.form.getlist('name')[0],
                            'phone':request.form.getlist('phone')[0],
                            'email':request.form.getlist('email')[0],
                            'gender':request.form.getlist('gender')[0],
                            'localId':"jjjdh"

                        }
                        user = auth.create_user_with_email_and_password(request.form.getlist('email')[0],request.form.getlist('password')[0])
                        data['localId'] = user['localId']
                        database.child("Users").child(user['localId']).child("Profile").set(data)
                        database.child("Users").child(user['localId']).child("Friends").child("novalue").set("dummy")
                        auth.send_email_verification(user['idToken'])
                        return render_template("sign-in.html", alert="true",
                                            message="Sign up successful! Please login.")
                    except Exception as e:
                        print(e)
                        return render_template("sign-in.html",alert="true",message="Cannot sign in. Seems username already exists")

                else:
                    return render_template("sign-in.html",alert="true",message="Password length should be greator than 6 characters and both the passwords should match")

        except Exception as e:
            pass
        return render_template("sign-in.html", message="Lets start making friends")


    @app.route("/accept/<id>")
    def accept(id):
        database.child("Users").child(id).child("Friends").child(session['user']).set("accepted")
        database.child("Users").child(session['user']).child("Friends").child(id).set("accepted")
        return redirect("/homepage")

    @app.route("/reject/<id>")
    def reject(id):
        database.child("Users").child(id).child("Friends").child(session['user']).remove()
        database.child("Users").child(session['user']).child("Friends").child(id).remove()
        return redirect("/homepage")


    @app.route("/homepage",methods=('GET','POST'))
    def homepage():


        try:
            username = database.child("Users").child(session['user']).child("Profile").child("name").get().val()
            print(username)
            friendsCount = database.child("Users").child(session['user']).child("Friends").get().val()
            if(friendsCount==None):
                friendsCount="."
            allUsers = getAllUsers()
            print(session['user'])
            friendsDict = getFriends(allUsers,session['user'])
            print(friendsDict)
            friendNames = suggestedFriends(friendsDict)
            pendingRequests = friendrequests()
            try:
                if (request.form.getlist('post')[0] == 'post'):
                    print("POST")
                    desc = request.form.getlist('description')
                    title = request.form.getlist('title')
                    data = {
                        'desc': desc[0],
                        'title': title[0]
                    }
                    currentTime = str(ts).replace(".", "-")
                    database.child("Posts").child(session['user']).child(currentTime).set(data)


            except Exception as e:
                print(" -- ", e)
            allPosts = database.child("Posts").get().val()
            postsdict={}
            for i in allPosts:

                print(i not in friendNames)
                if((i in friendNames)==True or session['user']==i):
                    for j in database.child("Posts").child(i).get().val():
                        postsdict[j] = [ database.child("Posts").child(i).child(j).child('desc').get().val() , database.child("Posts").child(i).child(j).child('title').get().val(), database.child("Users").child(i).child("Profile").child("name").get().val() ]
                else:
                    print("No")
            return render_template("homepage.html",username=username,friendsCount=len(friendsCount)-1,friendNames = friendNames,pendingRequests=pendingRequests,postsdict=postsdict)
        except Exception as e:
            print(e)

        return render_template("homepage.html",username=username,friendsCount=len(friendsCount)-1,friendNames = friendNames,pendingRequests=pendingRequests)


    def getAllUsers():
        usersDict = {}
        users = database.child("Users").get().val()
        for i in users:
            usersDict[i] = []
            for j in database.child("Users").child(i).child("Friends").get().val():
                friendshipStatus = database.child("Users").child(i).child("Friends").child(j).get().val()
                if(friendshipStatus=="accepted"):
                    usersDict[i].append(j)

        return usersDict

    @app.route("/friends")
    def friends():
        allUsers = getAllUsers()
        friendsDict = getFriends(allUsers, session['user'])
        friendNames = suggestedFriends(friendsDict)
        return render_template("friends.html",friendNames = friendNames)

    def suggestedFriends(friendsDict):
        userNames = {}
        for degree, ids in friendsDict.items():
            if(degree!=1):
                for i in ids:
                    name = database.child("Users").child(i).child("Profile").child("name").get().val()
                    if(degree==0):
                        userNames[i] = str(name) + str(3)
                    else:
                        userNames[i] = str(name) + str(degree)
        return userNames


    @app.route("/sendrequest/<id>")
    def sendRequest(id):
        database.child("Users").child(id).child("Friends").child(session['user']).set("Pending")
        database.child("Users").child(session['user']).child("Friends").child(id).set("PendingFromUser")
        return redirect("/homepage")


    def friendrequests():
        friendstree = database.child("Users").child(session['user']).child("Friends").get().val();
        idslist = []
        for i in friendstree:
            getFriendId = database.child("Users").child(session['user']).child("Friends").child(i).get().val();
            if(getFriendId=='Pending'):
                idslist.append([i,database.child("Users").child(i).child("Profile").child("name").get().val()])
        return idslist


    @app.route('/profile/<id>')
    def profile(id):
        gender = database.child("Users").child(id).child("Profile").child("gender").get().val()
        phone = database.child("Users").child(id).child("Profile").child('phone').get().val()
        email = database.child("Users").child(id).child("Profile").child('email').get().val()
        name = database.child("Users").child(id).child("Profile").child('name').get().val()

        friendsCount = database.child("Users").child(id).child("Friends").get().val()
        print(session['user'],id)

        roomID = id+session['user']
        if(session['user']<id):
            roomID = session['user']+id

        if (friendsCount == None):
            friendsCount = "."
        return render_template('userprofile.html',roomID=roomID,name=name,phone=phone,email=email,friendsCount=len(friendsCount)-1,userId=id,gender=gender)


    @app.route('/myfriends')
    def myfriends():
        friendNode = database.child("Users").child(session['user']).child("Friends").get().val()
        friends = {}
        for i in friendNode:
            print(i)
            if(i!='novalue'):
                name = database.child("Users").child(i).child("Profile").child("name").get().val()
                friends[i] = [name,"  "]
                if(database.child("Users").child(session['user']).child("Friends").child(i).get().val()!="accepted"):
                    friends[i][1] = "Pending"
        return render_template('myfriends.html',friends=friends)

        
    return app