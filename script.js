const config = {
	apiUrl: 'https://rub3fcpd3p.us-east-1.awsapprunner.com'
};

document.addEventListener('DOMContentLoaded', () => {
	const form = document.getElementById('letter-form');
	const previewBtn = document.getElementById('preview-btn');
	const previewModal = document.getElementById('preview-modal');
	const closeBtn = document.querySelector('.close');
	const letterPreview = document.getElementById('letter-preview');

	// Preview functionality
	previewBtn.addEventListener('click', () => {
		const sender = document.getElementById('sender').value;
		const receiver = document.getElementById('receiver').value;
		const content = document.getElementById('content').value;
		const isAnonymous = document.getElementById('anonymous').checked;

		letterPreview.innerHTML = `
			<div class="letter-content">
				<p class="letter-date">${new Date().toLocaleDateString()}</p>
				<p class="letter-to">Dear ${receiver},</p>
				<div class="letter-body">${content.replace(/\n/g, '<br>')}</div>
				<p class="letter-from">${isAnonymous ? 'Anonymous' : (sender || 'A Friend')}</p>
			</div>
		`;

		previewModal.style.display = 'block';
	});

	// Close preview modal
	closeBtn.addEventListener('click', () => {
		previewModal.style.display = 'none';
	});

	// Close modal when clicking outside
	window.addEventListener('click', (event) => {
		if (event.target === previewModal) {
			previewModal.style.display = 'none';
		}
	});

	// Handle form submission
	form.addEventListener('submit', async (event) => {
		event.preventDefault();

		const apiRequest = {
			sender: document.getElementById('sender').value,
			receiver: document.getElementById('receiver').value,
			content: document.getElementById('content').value,
			isAnonymous: document.getElementById('anonymous').checked,
			isPublic: document.getElementById('public').checked,
			expiryDays: document.getElementById('expiry').value
		};

		try {
			console.log('Sending data:', apiRequest);

			// Play paper sound effect
			const paperSound = new Audio('https://assets.mixkit.co/active_storage/sfx/2579/2579-preview.mp3');
			paperSound.play();

			// Show sending animation
			const sendBtn = document.getElementById('send-btn');
			sendBtn.disabled = true;
			sendBtn.textContent = 'Sending...';

			// Call Lambda function to save the letter
			const response = await fetch(`${config.apiUrl}/letter`, {
				method: 'POST',
				mode: 'cors',
				credentials: 'omit',
				headers: {
					'Content-Type': 'application/json',
					'Accept': 'application/json'
				},
				body: JSON.stringify(apiRequest)
			});

			console.log('Response status:', response.status);
			console.log('Response headers:', Object.fromEntries(response.headers));
			
			const data = await response.json().catch(e => ({ error: 'Failed to parse response' }));
			console.log('Response data:', data);

			if (response.ok && data.success) {
				// Show success message with the letter URL
				alert(`Your letter has been sent! Share this link: ${data.letterUrl}`);
				form.reset();
			} else {
				throw new Error(data.error || 'Failed to send letter');
			}
		} catch (error) {
			console.error('Error details:', error);
			alert('Error sending letter: ' + error.message);
		} finally {
			const sendBtn = document.getElementById('send-btn');
			sendBtn.disabled = false;
			sendBtn.textContent = 'Send Chitthi';
		}
	});

	// Add paper sound effect when typing
	const contentTextarea = document.getElementById('content');
	let lastTypedTime = 0;
	const paperSound = new Audio('https://assets.mixkit.co/active_storage/sfx/2579/2579-preview.mp3');

	contentTextarea.addEventListener('input', () => {
		const currentTime = Date.now();
		if (currentTime - lastTypedTime > 1000) { // Play sound every second
			paperSound.currentTime = 0;
			paperSound.play();
			lastTypedTime = currentTime;
		}
	});
});

const counter = document.querySelector(".counter-number");
async function updateCounter() {
	let response = await fetch(
		"https://o73g5ptpujgtclinhzhhneplje0jogoh.lambda-url.us-east-1.on.aws/"
	);
	let data = await response.json();
	counter.innerHTML = `Views: ${data}`;
}
updateCounter();
