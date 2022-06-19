class NoteEventhandler{
	constructor(commentsDiv, responseForm) {
		this.eventDispatcher = this.eventDispatcher.bind(this);
		this.commentsDiv = commentsDiv;
		this.commentsDiv.after(responseForm);
		this.responseForm = responseForm;
	}
	eventHandler() {
		this.commentsDiv.addEventListener('click', this.eventDispatcher);
		window.addEventListener('load', this.eventDispatcher);
		this.commentsDiv.querySelector('.comment-list').addEventListener('mouseover', this.eventDispatcher);
	}
	eventDispatcher(event) {
		switch (event.type) {
			case 'click':
				if (event.target.closest('.response-note')) {
					event.preventDefault();
					let elem = event.target.closest('.response-note');
					this.createCommentForm(elem);
				} else if (event.target.closest('.note-likes')) {
					let elem = event.target.closest('.note-likes');
					this.addLike(elem);
				}
				break
			case 'load':
				let elem = document.querySelector('.note-views');
				this.addView(elem);
				document.removeEventListener('load', this.eventDispatcher);
				break
			case 'mouseover':
				if (event.target.closest('.note-views')) {
					let elem = event.target.closest('.note-views')
					this.addView(elem);
				}
				break
			default:
				break
		}
	}
	createCommentForm(elem) {
		this.responseForm.querySelector('#id_post').value = elem.id
		if (elem.parentNode.classList.contains('comment-head')) {
			elem.parentNode.after(this.responseForm);
		} else {
			elem.after(this.responseForm);
		}
		this.responseForm.hidden = false;
	}
	addLike(elem) {
		let request = this.getNotePatchRequest(elem.id);
		let data = {
			'likes': [JSON.parse(document.getElementById('user').textContent)],
			'views': [JSON.parse(document.getElementById('session').textContent)],
		};
		request.send(JSON.stringify(data));
		let _this = this;
		request.onreadystatechange = function () {
			if (request.readyState == 4 && request.status == 200) {
				let note_data = JSON.parse(request.response);
				_this.updateNoteData(elem, note_data)
			}
		}
	}
	addView(elem) {
		let request = this.getNotePatchRequest(elem.id);
		let data = {
			'views': [JSON.parse(document.getElementById('session').textContent)],
		};
		request.send(JSON.stringify(data));
		let _this = this;
		request.onreadystatechange = function () {
			if (request.readyState == 4 && request.status == 200) {
				let note_data = JSON.parse(request.response);
				_this.updateNoteData(elem, note_data);
			}
		}
	}
	getCookie(name) {
		const value = `; ${document.cookie}`;
		const parts = value.split(`; ${name}=`);
		if (parts.length === 2) return parts.pop().split(';').shift();
	}
	getNotePatchRequest(id) {
		const url = `/api/notes/update/${id}`;
		let request = new XMLHttpRequest();
		request.open('PATCH', url);
		request.setRequestHeader('Content-Type', 'application/json');
		request.setRequestHeader("X-CSRFToken", this.getCookie('csrftoken'));
		return request
	}
	updateNoteData(elem, data) {
		let likes = elem.parentNode.querySelector('.likes-value');
		let views = elem.parentNode.querySelector('.views-value');
		likes.textContent = data['note']['likes'];
		views.textContent = data['note']['views'];
	}
}
commentsDiv = document.querySelector('.comments');
formScript = document.querySelector('#response-form-div');
noteResponseHandler = new NoteEventhandler(commentsDiv, formScript);
noteResponseHandler.eventHandler();