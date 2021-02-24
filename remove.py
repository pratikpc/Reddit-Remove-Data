import praw
import os

from dotenv import load_dotenv
load_dotenv()

reddit_client_id, reddit_client_secret = os.environ["CLIENT_ID"], os.environ["CLIENT_SECRET"]
reddit_user_name, reddit_user_pass = password = os.environ[
    "REDDIT_USER"], os.environ["REDDIT_PASSWORD"]


reddit = praw.Reddit(client_id=reddit_client_id,
                     client_secret=reddit_client_secret,
                     password=reddit_user_pass,
                     user_agent="Clear Reddit History",
                     username=reddit_user_name)

# Get the Current User
user = reddit.user.me()

# Remove Comments
while True:
    comment_ids = [comment.id for comment in user.comments.new(limit=None)]

    if(len(comment_ids) == 0):
        break

    print("Start deleting", len(comment_ids), "comments")

    for id in comment_ids:
        try:
            reddit.comment(id=id).edit("##")
        except:
            pass
        reddit.comment(id=id).delete()

# Remove Posts
while True:
    post_ids = [post.id for post in user.submissions.new(limit=None)]

    if(len(post_ids) == 0):
        break

    print("Start deleting", len(post_ids), "posts")

    for id in post_ids:
        reddit.submission(id=id).delete()

# count_errs explained
# Every time there is an error
# This could imply that the resource in question cannot be removed
# Due to the 6 month policy
# So we increment error count
# To ensure we don't enter an infinite loop
# If count_err is same as number of items found
# This means that these items cannot be removed

# Remove votes
count_errs = 0
while True:

    voted_ids = [vote.id for vote in user.upvoted(
        limit=None)] + [vote.id for vote in user.downvoted(limit=None)]

    if(len(voted_ids) == count_errs):
        break

    print("Start deleting", len(voted_ids), "votes")

    for id in voted_ids:
        try:
            reddit.submission(id=id).clear_vote()
        except:
            count_errs = count_errs + 1

# Remove Hidden
while True:
    hidden_ids = [item.id for item in user.hidden(limit=None)]

    if(len(hidden_ids) == 0):
        break

    print("Start deleting", len(hidden_ids), "hidden")

    for id in hidden_ids:
        reddit.submission(id=id).unhide()

# Remove Saved
while True:
    saved = [save for save in user.saved(limit=None)]

    saved_comment_ids = [
        save.id for save in saved if isinstance(save, praw.models.Comment)]
    saved_post_ids = [save.id for save in saved if isinstance(
        save, praw.models.Submission)]

    if(len(saved_post_ids) + len(saved_comment_ids) == 0):
        break

    print("Start deleting", len(saved_post_ids) +
          len(saved_comment_ids), "saved")

    for id in saved_comment_ids:
        reddit.comment(id=id).unsave()
    for id in saved_post_ids:
        reddit.submission(id=id).unsave()
