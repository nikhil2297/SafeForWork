document.addEventListener('DOMContentLoaded', function() {
    const commentInput = document.getElementById('comment-input');
    const submitButton = document.getElementById('submit-comment');
    const commentContainer = document.querySelector('.comment-container');

    submitButton.addEventListener('click', function() {
        const comment = commentInput.value.trim();
        console.log(comment);

        if (comment !== '') {
            fetch('/add_tweet', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({tweet: comment})
            })
            .then(response => response.json())
            .then(data => {
                const newComment = document.createElement('p');
                newComment.classList.add('card-comment');
                if (data.sentiment > 0.4) {
                    newComment.classList.add('blur-comment');
                } else {
                    newComment.classList.add('regular');
                }
                newComment.textContent = data.tweet;
                commentContainer.insertBefore(newComment, commentContainer.firstChild);
                commentInput.value = '';
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }else {
            console.log('Empty comment');
        }
    });
});