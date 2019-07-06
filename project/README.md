#### CS50 Final project
# My WordNote
raeazalea (edx ID)

My final project is called 'My WordNote'.  
This is for learning English words.   
It let the users search the words using 'Naver dictionary', write the meaning of the words in their own words and practice them.  

----------------------------
This project has the same foundation as CS50 pset8: Finance has.  
<br>
Here is the list of files from 'pset8: Finance' with no revisal.  
<br>

1. `templates`
    - `apology.html`
    - `login.html`
    - `register.html`
    - `layout.html` (revised a little bit)

2. `application.py`
    - `register`
    - `logon`
    - `logout`
    - `check`

3. `help.py`
    - `apology`
    - `login_required`

4. `static`

5. `requirements.txt`

--------------------------------
Here are the new features of 'My WordNote'.  
<br>

1. ** search ** / ** makenote **
    - Make two templates : `search.html`, `meaning.html`
    - In `search.html`, make input for the word.
    - In `meaning.html`, it shows the search result of the word the user submitted through input.   
        Divide the page into two columns, one side is for the 'Naver dictionary' display. Used `<iframe>`  
        and the other side if for making the user create wordnote in their own words.
        
    - In `application.py` make `search` function.
    - Check if the submit the word. if not, apologize.
    - When the word is submitted, `render_template("meaning.html")`
    - And, make `makenote` function.
    - `makenote` function saves user's input into `words` in `wordnote.db`. (make `words` table in `wordnote.db`)
    - Make sure that the inputs are not blank. If the user save the same word, apologize.
    - When submitted, `INSERT INTO words`, flash and `redirect("/")`

2. ** mynote ** 
    - `mynote.html` shows the table of words and its meanings.
    - Use Jinja to iterate the rows for the table.
    - Make `mynote` function to select data from the `words`.
    - Add `delete` button on each row to delete selected row only.
    - `<button class="btn btn-outline-dark btn-sm" name="delete" value="{{word["id"]}}" type="submit">Delete</button>`
    - Use POST method. When `request.form.get("delete")` happens `mynote`fuction takes the value (id of the word in `words`table) and `DELETE FROM words`.

3. ** quiz **
    - In `quiz.html`, there are two divisions.
    - One `div` is jumbotron (bootstrap). It asks the question to the user.
    - The other `div` is for `answer` input.
    - In `application.py`, make `quiz` function.
    - If the method is `GET`, make the list of the words' id and choose one randomly. When the list is empty, apologize.
    - `from random import choice` --> choose one element from the list randomly.
    - If the method is `POST`, first, ensure the answer is submitted. If not, apologize.
    - Check if the answer is right or not.
    - _reminder_ : the variable `quiz` under `if request.method == "GET":` is local variable. Can't be used when the method is `POST`.
    - So, make hidden input in `quiz.html` to send the value of 'word' (name="checking") when submitted. Then we can check the answer simply using `request.form.get("answer") != request.form.get("checking")`.
    -  For Correct answer rate, when the answer is wrong `UPDATE` the `quiz_total` by 1, when the answer is right `UPDATE` the `quiz_total` and `quiz_corr`.
    -  Then, flash the result and `redirect("/")`.
4. ** index **
    - Make `index.html`. Show the user ID who is logging in currently and the the correct answer rate. (Add progress bar)
    - And make the description of the website.