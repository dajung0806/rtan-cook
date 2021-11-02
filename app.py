from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# client = MongoClient('mongodb://test:test@localhost', 27017)
client = MongoClient("localhost", 27017)
db = client.dbmaking


# HTML 화면 표시
@app.route("/")
def init():
    return render_template("index.html")

# 회원가입 페이지
@app.route("/register")
def sign_up():
    return render_template("register.html")

# 로그인 페이지
@app.route("/login")
def sign_in():
    return render_template("login.html")


# 멤버 소개 페이지
@app.route("/about")
def about_page():
    return render_template("about.html")


# 상위 레시피 표시
@app.route("/rank/favorite", methods=["GET"])
def show_favorite():
    favorite_list = list(db.recipes.find({}, {"_id": False}).sort("like", -1).limit(4))
    return jsonify({"favorite_Lists": favorite_list})


# 전체 요리 레시피 순위 페이지
@app.route("/rank")
def rank_page():
    return render_template("rank.html")


@app.route("/rank/list", methods=["GET"])
def show_rank():
    recipe_list = list(db.recipes.find({}, {"_id": False}).sort("like", -1))
    return jsonify({"recipe_Lists": recipe_list})


@app.route("/rank/sort", methods=["GET"])
def show_sort():
    sort_list = list(db.recipes.find({}, {"_id": False}).sort("name", 1))
    return jsonify({"sort_lists": sort_list})


# 요리 레시피 리스트 요청
@app.route("/recommend")
def recommend_page():
    return render_template("recommend.html")


@app.route("/recipe")
def recipe_page():
    return render_template("recipe.html")


@app.route("/recommend/search", methods=["POST"])
def search_1to2():
    ingredients = request.form
    ingredients = ingredients.getlist("ing_list")
    print(ingredients)
    db.search.update_one({"name": "검색"}, {"$set": {"index": ingredients}})
    return jsonify({"msg": "저장"})


@app.route("/recommend/read", methods=["GET"])
def search():
    search = db.search.find_one({"name": "검색"})
    recipes = list(
        db.recipes.find({"search": {"$all": search["index"]}}, {"_id": False}).sort(
            "like", -1
        )
    )
    # recipes = list(db.recipes.find({'search':ingredients},{'_id':False}))
    # recipes = list(db.recipes.find({'search':search['index']},{'_id':False}))
    return jsonify({"recipes": recipes})


@app.route("/recommend/ingredient", methods=["GET"])
def search_ing():
    search = db.search.find_one({"name": "검색"}, {"_id": False})
    return jsonify({"ing": search})


@app.route("/recommend/search2", methods=["POST"])
def search_2to3():
    name = request.form["name_give"]
    db.search.update_one({"name": "검색2"}, {"$set": {"index": name}})
    return jsonify({"msg": "저장"})


@app.route("/recipe/read", methods=["GET"])
def search2():
    search = db.search.find_one({"name": "검색2"})
    # recipes = list(db.recipes.find({'search': {'$all':ingredients}},{'_id':False}))
    # recipes = list(db.recipes.find({'search':ingredients},{'_id':False}))
    recipe = db.recipes.find_one({"name": search["index"]}, {"_id": False})
    return jsonify({"recipes": recipe})


# 요리 레시피 요청
# @app.route('/recipe', methods=['GET'])
# def show_recipe():
#     sample_receive = request.args.get('sample_give')
#     print(sample_receive)
#     return jsonify({'msg': 'list 연결되었습니다!'})


@app.route("/recipe", methods=["GET"])
def recipe():
    name_receive = db.recipes.find_one({"name": "계란찜 [Gyeran-jjim]"})
    print(name_receive)
    return jsonify({"msg": "list 연결되었습니다!"})


#
# ingredients = ['계란','물','소금']
# test = list(db.recipes.find({'search': {'$all':ingredients}},{'_id':False}))
# print(test,len(test))

# 좋아요 싫어요
@app.route("/recipe/like", methods=["POST"])
def like_star():
    name_receive = request.form["name_give"]

    target_star = db.recipes.find_one({"name": name_receive})
    current_like = target_star["like"]

    new_like = current_like + 1

    db.recipes.update_one({"name": name_receive}, {"$set": {"like": new_like}})

    return jsonify({"msg": "좋아요!"})


@app.route("/recipe/hate", methods=["POST"])
def hate_star():
    name_receive = request.form["name_give"]

    target_star = db.recipes.find_one({"name": name_receive})
    current_like = target_star["like"]

    hate_like = current_like - 1

    db.recipes.update_one({"name": name_receive}, {"$set": {"like": hate_like}})

    return jsonify({"msg": "싫어요!"})


@app.route("/login/check", methods=["POST"])
def login():
    userid_receive = request.form["userid_give"]
    userpw_receive = request.form["userpw_give"]

    target = db.users.find_one(
        {"user_id": userid_receive, "user_pw": userpw_receive}, {"_id": False}
    )
    print(target)
    return jsonify({"user_data": target})


@app.route("/register/add", methods=["POST"])
def register():
    userid_receive = request.form["userid_give"]
    userpw_receive = request.form["userpw_give"]
    usermail_receive = request.form["usermail_give"]

    doc = {
        "user_id": userid_receive,
        "user_pw": userpw_receive,
        "user_mail": usermail_receive,
    }

    db.users.insert_one(doc)

    return jsonify({"msg": "가입완료"})


# 추천 요리 표시

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)
