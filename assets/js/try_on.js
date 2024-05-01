   // static/js/try_on.js



let currentShirt = 0;

async function setupCamera() {
	const video = document.getElementById("video");
	const stream = await navigator.mediaDevices.getUserMedia({
		video: true,
	});
	video.srcObject = stream;
	return new Promise((resolve) => {
		video.onloadedmetadata = () => {
			resolve(video);
		};
	});
}

async function loadPosenet() {
	const net = await posenet.load();
	const video = await setupCamera();
	video.play();
	detectPose(net, video);
}

function detectPose(net, video) {
	const canvas = document.getElementById("canvas");
	const ctx = canvas.getContext("2d");
	async function poseDetectionFrame() {
		const pose = await net.estimateSinglePose(video, {
			flipHorizontal: false,
		});
		drawResult(pose, video, ctx);
		requestAnimationFrame(poseDetectionFrame);
	}
	poseDetectionFrame();
}

function drawResult(pose, video, ctx) {
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.drawImage(video, 0, 0, 640, 700); // Assuming video height adjusted to 720

	if (pose.keypoints[5].score > 0.5 && pose.keypoints[6].score > 0.5) {
		const leftShoulder = pose.keypoints[5].position;
		const rightShoulder = pose.keypoints[6].position;

		const centerX = (leftShoulder.x + rightShoulder.x) / 2;
		const centerY = (leftShoulder.y + rightShoulder.y) / 2;
		const shoulderWidth = Math.abs(leftShoulder.x - rightShoulder.x);

		const shirtWidth = shoulderWidth * 2.5; // Adjust this factor based on your needs
		const img = new Image();
		img.src = shirtImages[currentShirt];
		img.onload = () => {
			const shirtHeight = img.height * (shirtWidth / img.width);

			const shirtStartX = centerX - shirtWidth / 2;
			// Adjust the Y position to start lower since centerY is at the midpoint of the shoulders
			const shirtStartY = centerY - shirtHeight * -.1; // Start the shirt slightly above the center

			ctx.drawImage(img, shirtStartX, shirtStartY, shirtWidth, shirtHeight);
		};
	}
}



function changeShirt(direction) {
	currentShirt += direction;
	if (currentShirt >= shirtImages.length) {
		currentShirt = 0;
	} else if (currentShirt < 0) {
		currentShirt = shirtImages.length - 1;
	}
}

loadPosenet();