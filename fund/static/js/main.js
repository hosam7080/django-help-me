(function () {
	'use strict';
	var forms = document.querySelectorAll('.needs-validation');
	Array.prototype.slice.call(forms).forEach(function (form) {
		form.addEventListener('submit', function (event) {
			if (!form.checkValidity()) {
				event.preventDefault();
				event.stopPropagation();
			}
			form.classList.add('was-validated');
		}, false);
	});
})();

/* ======== Add Modal: Tags Logic ======== */
let addTagBtn = document.getElementById('addTagBtn')
	if (addTagBtn) {
		addTagBtn.addEventListener('click', function () {
			var select = document.getElementById('addTagsSelect');
			var selectedValue = select.value;
			var selectedText = select.options[select.selectedIndex].text;
			if (selectedValue === "") return;
			var container = document.getElementById('selectedTagsContainer');
			if (container.querySelector('[data-tag-id="' + selectedValue + '"]')) return;
			var badge = document.createElement('span');
			badge.className = 'badge bg-primary me-1';
			badge.textContent = selectedText;
			badge.setAttribute('data-tag-id', selectedValue);
			badge.style.cursor = 'pointer';
			badge.addEventListener('click', function () {
				this.remove();
				updateAddTagsInput();
			});
			container.appendChild(badge);
			updateAddTagsInput();
		});
	}

function updateAddTagsInput() {
	var tags = [];
	document.querySelectorAll('#selectedTagsContainer span').forEach(function (el) {
		tags.push(el.getAttribute('data-tag-id'));
	});
	document.getElementById('selectedTagsInput').value = tags.join(',');
}

/* ======== Update Modal: Tags Logic ======== */
let updateTagBtn = document.getElementById('updateTagBtn')

if (updateTagBtn) {

	updateTagBtn.addEventListener('click', function () {
		var select = document.getElementById('updateTagsSelect');
		var selectedValue = select.value;
		var selectedText = select.options[select.selectedIndex].text;
		if (selectedValue === "") return;
		var container = document.getElementById('updateSelectedTagsContainer');
		if (container.querySelector('[data-tag-id="' + selectedValue + '"]')) return;
		var badge = document.createElement('span');
		badge.className = 'badge bg-primary me-1';
		badge.textContent = selectedText;
		badge.setAttribute('data-tag-id', selectedValue);
		badge.style.cursor = 'pointer';
		badge.addEventListener('click', function () {
			this.remove();
			updateUpdateTagsInput();
		});
		container.appendChild(badge);
		updateUpdateTagsInput();
	});
}
function updateUpdateTagsInput() {
	var tags = [];
	document.querySelectorAll('#updateSelectedTagsContainer span').forEach(function (el) {
		tags.push(el.getAttribute('data-tag-id'));
	});
	document.getElementById('updateSelectedTagsInput').value = tags.join(',');
	checkUpdateChanges();
}

/* ======== Update Modal: Check for Changes ======== */
var initialUpdateData = {};
function checkUpdateChanges() {
	var currentData = {
		title: document.getElementById('updateTitle').value,
		details: document.getElementById('updateDetails').value,
		total_target: document.getElementById('updateTotalTarget').value,
		start_time: document.getElementById('updateStartTime').value,
		end_time: document.getElementById('updateEndTime').value,
		category: document.getElementById('updateCategory').value,
		tags: document.getElementById('updateSelectedTagsInput').value
	};
	var hasChanged = Object.keys(initialUpdateData).some(function (key) {
		return initialUpdateData[key] !== currentData[key];
	});
	document.getElementById('updateSubmitBtn').disabled = !hasChanged;
}

/* ======== Update Modal: Populate Data ======== */
var updateModal = document.getElementById('updateProjectModal');
if (updateModal) {

	updateModal.addEventListener('show.bs.modal', function (event) {
		var button = event.relatedTarget;
		var projectId = button.getAttribute('data-id');
		var title = button.getAttribute('data-title');
		var details = button.getAttribute('data-details');
		var totalTarget = button.getAttribute('data-total_target');
		var startTime = button.getAttribute('data-start_time');
		var endTime = button.getAttribute('data-end_time');
		var category = button.getAttribute('data-category');
		var tags = button.getAttribute('data-tags').split(',');

		document.getElementById('updateProjectId').value = projectId;
		document.getElementById('updateTitle').value = title;
		document.getElementById('updateDetails').value = details;
		document.getElementById('updateTotalTarget').value = totalTarget;
		document.getElementById('updateStartTime').value = startTime;
		document.getElementById('updateEndTime').value = endTime;
		document.getElementById('updateCategory').value = category;

		var updateContainer = document.getElementById('updateSelectedTagsContainer');
		updateContainer.innerHTML = "";
		tags.forEach(function (tagId) {
			if (tagId.trim() !== "") {
				var option = document.querySelector('#updateTagsSelect option[value="' + tagId + '"]');
				if (option) {
					var badge = document.createElement('span');
					badge.className = 'badge bg-primary me-1';
					badge.textContent = option.text;
					badge.setAttribute('data-tag-id', tagId);
					badge.style.cursor = 'pointer';
					badge.addEventListener('click', function () {
						this.remove();
						updateUpdateTagsInput();
					});
					updateContainer.appendChild(badge);
				}
			}
		});
		updateUpdateTagsInput();

		initialUpdateData = {
			title: title,
			details: details,
			total_target: totalTarget,
			start_time: startTime,
			end_time: endTime,
			category: category,
			tags: document.getElementById('updateSelectedTagsInput').value
		};

		document.getElementById('updateProjectForm').action = "{% url 'project_update' 0 %}".replace("0", projectId);
		document.getElementById('updateSubmitBtn').disabled = true;
	});
}
let updateProjectForm = document.getElementById('updateProjectForm')
if (updateProjectForm) {

	updateProjectForm.addEventListener('input', checkUpdateChanges);
}

/* ======== Delete Modal Setup ======== */
var deleteConfirmModal = document.getElementById('deleteConfirmModal');
if (deleteConfirmModal){

deleteConfirmModal.addEventListener('show.bs.modal', function (event) {
	var projectId = document.getElementById('updateProjectId').value;
	document.getElementById('deleteProjectId').value = projectId;
	document.getElementById('deleteProjectForm').action = "{% url 'project_delete' 0 %}".replace("0", projectId);
});
}
(function () {
	'use strict';
	window.addEventListener('load', function () {
		var forms = document.getElementsByClassName('needs-validation');
		Array.prototype.forEach.call(forms, function (form) {
			form.addEventListener('submit', function (event) {
				if (!form.checkValidity()) {
					event.preventDefault();
					event.stopPropagation();
				}
				form.classList.add('was-validated');
			}, false);
		});
	}, false);
})();



// document.addEventListener("DOMContentLoaded", function () {
// 	let editButtons = document.querySelectorAll(".edit-btn");
// let updateForm = document.getElementById("updateProjectForm");

// 	editButtons.forEach((button) => {
// 	button.addEventListener("click", function () {
// 		let projectId = this.dataset.id;
// 		let title = this.dataset.title;
// 		let details = this.dataset.details;
// 		let totalTarget = this.dataset.total_target;
// 		let startTime = this.dataset.start_time;
// 		let endTime = this.dataset.end_time;
// 		let category = this.dataset.category;
// 		let tags = this.dataset.tags.split(",");

// 		document.getElementById("updateProjectId").value = projectId;
// 		document.getElementById("updateTitle").value = title;
// 		document.getElementById("updateDetails").value = details;
// 		document.getElementById("updateTotalTarget").value = totalTarget;
// 		document.getElementById("updateStartTime").value = startTime;
// 		document.getElementById("updateEndTime").value = endTime;
// 		document.getElementById("updateCategory").value = category;

// 		// Populate selected tags
// 		let tagsInput = document.getElementById("updateSelectedTagsInput");
// 		tagsInput.value = tags.join(",");

// 		updateForm.action = `/update-project/${projectId}/`;
// 	});
// 	});
// });




