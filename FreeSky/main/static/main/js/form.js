class FormObserver {
	constructor(form, textInputs) {
		this.form = form;
		this.mainPage = form.parentNode.parentNode.parentNode;
		this.textInputElems = textInputs;
		this.eventDispatcher = this.dispatchHandler.bind(this)
		this.choiceDiv = this.createChoiceDiv();
		this.resultDiv = this.createSearchResultDiv();
		this.data;
	}
	createChoiceDiv() {
		let div = document.createElement('div');
		div.classList.add('choice_ui');
		return div
	}
	createSearchResultDiv() {
		let div = document.createElement('div');
		div.classList.add('main__search-result')
		div.classList.add('search-result')
		return div
	}
	eventHandler() {
		this.form.addEventListener('submit', this.eventDispatcher)
		this.form.addEventListener('input', this.eventDispatcher)
		this.form.addEventListener('focus', this.eventDispatcher)
		this.form.addEventListener('blur', this.eventDispatcher)
		this.form.addEventListener('click', this.eventDispatcher)
		this.resultDiv.addEventListener('click', this.eventDispatcher)
	}
	dispatchHandler(event) {
		switch (event.type) {
			case 'input':
				if (event.target.closest('.search_ui')) {
					let elem = event.target.closest('.search_ui');
					if (elem.value.length > 0) {
						this.getTypingRequest(elem);
					}
					elem.after(this.choiceDiv);
				}
				break
			case 'blur':
				this.choiceDiv.remove();
				break
			case 'click':
				if (event.target.closest('.choice_element')) {
					let text = event.target.closest('.choice_element');
					let input = text.parentNode.previousElementSibling;
					input.value = text.innerText;
				} else if (!event.target.closest('.button-selected') && event.target.closest('.paggination-button')) {
					let page = event.target.closest('.paggination-button');
					let value = page.value - 1;
					this.getSubmitResponse(this.data, value);
				}
				break
			case 'submit':
				event.preventDefault();
				let data = new FormData(this.form);
				this.getSubmitRequest(data);
				break
			default:
				break
		}
	}
	getTypingRequest(inputElement) {
		let myRequest = new XMLHttpRequest();
		myRequest.open('GET', `/api/search?text=${inputElement.value}`, true);
		myRequest.responseType = 'json'
		myRequest.send();
		let _this = this;
		myRequest.onreadystatechange = function () {
			if (myRequest.readyState == 4 && myRequest.status == 200) {
				_this.updateChoiceDivData(myRequest.response)
			}
		}
	}
	updateChoiceDivData(responseData) {
		this.choiceDiv.textContent = ''
		let data = responseData["settlements"];
		for (let i in data) {
			let choiceElement = document.createElement('p');
			choiceElement.textContent = data[i]['name'];
			choiceElement.classList.add('choice_element');
			this.choiceDiv.append(choiceElement);
		}
	}
	getSubmitRequest(data) {
		let request = new XMLHttpRequest();
		request.responseType = "json";
		request.open('POST', '/api/search', true);
		request.send(data);
		let _this = this;
		request.onreadystatechange = function () {
			if (request.readyState == 4 && request.status == 200) {
				_this.data = request.response;
				console.log(_this.data)
				_this.getSubmitResponse(request.response);
			}
		}
	}
	getSubmitResponse(responseData, page=0) {
		this.resultDiv.textContent = '';
		this.resultDiv.remove();
		this.resultDiv.innerHTML = responseData['context'][page]
		this.mainPage.after(this.resultDiv);
	}
}

const observer = new FormObserver(document.querySelector('._form'),
	document.querySelectorAll('.search_ui'));
observer.eventHandler();
