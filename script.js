// 目标时间：新年（1月1日00:00:00）
const targetDate = new Date(new Date().getFullYear() + 1, 0, 1, 0, 0, 0);

// 获取页面元素
const countdownElement = document.getElementById("countdown");
const newYearMessage = document.getElementById("newYearMessage");

// 更新倒计时的函数
function updateCountdown() {
    const now = new Date();
    const timeDiff = targetDate - now;

    if (timeDiff <= 0) {
        // 倒计时结束
        countdownElement.style.display = "none";
        newYearMessage.style.display = "block";
        showFireworks();
        clearInterval(timer);
    } else {
        // 计算天、小时、分钟、秒
        const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((timeDiff / (1000 * 60 * 60)) % 24);
        const minutes = Math.floor((timeDiff / (1000 * 60)) % 60);
        const seconds = Math.floor((timeDiff / 1000) % 60);

        // 更新页面显示
        countdownElement.textContent = `${days} 天 ${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
}

// 每秒更新一次倒计时
const timer = setInterval(updateCountdown, 1000);
updateCountdown();

// 烟花效果（可选）
function showFireworks() {
    const canvas = document.getElementById("fireworksCanvas");
    const ctx = canvas.getContext("2d");

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff"];

    function createParticle(x, y) {
        return {
            x,
            y,
            vx: (Math.random() - 0.5) * 4,
            vy: (Math.random() - 0.5) * 4,
            color: colors[Math.floor(Math.random() * colors.length)],
            life: 100
        };
    }

    function drawParticles() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        particles.forEach((p, i) => {
            ctx.beginPath();
            ctx.arc(p.x, p.y, 3, 0, Math.PI * 2);
            ctx.fillStyle = p.color;
            ctx.fill();

            // 更新粒子位置
            p.x += p.vx;
            p.y += p.vy;
            p.life--;

            // 移除寿命结束的粒子
            if (p.life <= 0) particles.splice(i, 1);
        });
    }

    function spawnParticles() {
        for (let i = 0; i < 20; i++) {
            const x = Math.random() * canvas.width;
            const y = Math.random() * canvas.height / 2;
            particles.push(createParticle(x, y));
        }
    }

    function animate() {
        drawParticles();
        spawnParticles();
        requestAnimationFrame(animate);
    }

    animate();
}
