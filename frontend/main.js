let analysisMode = "lex";  // default: sólo léxico

/* ---------- gestor de tema ---------- */
document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('themeBtn');

    function applyTheme(mode) {
        if (mode === 'light') {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('theme', 'light');
            themeBtn.textContent = '☀️ Tema';
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('theme', 'dark');
            themeBtn.textContent = '🌑 Tema';
        }
    }

    document.querySelectorAll(".mode-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            analysisMode = btn.dataset.mode;

            // Resetear estilos de todos los botones
            document.querySelectorAll(".mode-btn").forEach(b => {
                b.classList.remove("ring-2", "text-blue-500", "dark:text-blue-400", "bg-white");
            });

            // Estilo activo al botón seleccionado
            btn.classList.add("ring-2", "text-blue-500", "dark:text-blue-400", "bg-white");

            // Limpia resultados anteriores
            document.getElementById("output").innerHTML = "";
        });
    });

    applyTheme(localStorage.getItem('theme') || 'dark');

    // Alterna entre claro y oscuro al hacer clic
    themeBtn.addEventListener('click', () => {
        const currentTheme = localStorage.getItem('theme');
        applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    });

    // Eventos para los botones
    document.getElementById("analyzeBtn").addEventListener("click", () => {
        analyzeCode();
    });

    document.getElementById("exampleBtn").addEventListener("click", () => {
        loadExample();
    });

    document.getElementById("uploadBtn").addEventListener("click", () => {
        document.getElementById("fileInput").click();
    });

    document.getElementById("clearBtn").addEventListener("click", () => {
        document.getElementById("codeInput").value = "";
        document.getElementById("output").innerHTML = "";
    });

    document.getElementById("downloadBtn").addEventListener("click", () => {
        const blob = new Blob([document.getElementById("output").innerText], { type: "text/plain" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "resultado.txt";
        a.click();
        URL.revokeObjectURL(url);
    });
});

function traducirError(msg) {
    const catalogo = [
        {
            pattern: /Expected IDENTIFIER but got KEYWORD/i,
            human: "Se esperaba un <strong>identificador</strong> pero se encontró una palabra reservada. " +
                "Revisa que no estés usando una palabra clave (por ejemplo <code>def</code>, <code>return</code>, etc.) " +
                "donde debería ir el nombre de una variable o función."
        },
        {
            pattern: /UnboundLocalError.*?total_tokens/i,
            human: "El compilador interno intentó usar la variable <code>total_tokens</code> antes de inicializarla. " +
                "Es un problema de la lógica del analizador, no de tu código fuente. " +
                "Informa al equipo de desarrollo."
        },
        {
            pattern: /SyntaxError/i,
            human: "Hay un error de sintaxis en tu código. Verifica paréntesis, dos puntos y sangrías."
        }
    ];

    for (const { pattern, human } of catalogo) {
        if (pattern.test(msg)) return human;
    }
    return `Detalle técnico: ${msg}`;
}

async function analyzeCode(code = null) {
    if (!code) code = document.getElementById("codeInput").value;

    const outputDiv = document.getElementById("output");
    const loadingDiv = document.getElementById("loading");

    outputDiv.innerHTML = "";
    loadingDiv.classList.remove("hidden");

    try {
        const resp = await fetch("http://localhost:5000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ code, mode: analysisMode })
        });
        const data = await resp.json();
        loadingDiv.classList.add("hidden");

        if (resp.ok) {
            if (analysisMode === "asm") {
                outputDiv.innerHTML = `<h2 class='text-lg font-bold mb-2'>Resultado del Ensamblador:</h2>`;

                outputDiv.innerHTML +=
                    `<p class="mt-2"><strong>Registros:</strong></p>
        <pre class="bg-gray-900 text-green-300 p-2 rounded">
        ${JSON.stringify(data.registers, null, 2)}
        </pre>`;

                outputDiv.innerHTML +=
                    `<p class="mt-2"><strong>Salida:</strong></p>
        <pre class="bg-gray-900 text-yellow-300 p-2 rounded">
        ${data.output.join('\n')}
        </pre>`;
                return;
            }

            Object.entries(data.counts).forEach(([cat, qty]) => {
                const vals = data.tokens[cat].join(", ");
                outputDiv.innerHTML +=
                    `<p><strong>${cat} (${qty}):</strong> ${qty ? vals : "<span class='text-yellow-400'>⚠ No se encontraron tokens.</span>"}</p>`;
            });

            outputDiv.innerHTML += `<p class="mt-2"><strong>Total de tokens:</strong> ${data.total_tokens}</p>`;

            if ((analysisMode === "full") || (analysisMode === "sem" && (!data.semantics || data.semantics.length === 0))) {
                outputDiv.innerHTML += `
        <hr class="section-divider"> <h2 class='text-lg font-bold text-center mt-4 leading-tight'>Árbol de Sintaxis (AST) <span class="tooltip text-xs align-middle opacity-70 ml-1" title="Representación jerárquica del código fuente">🛈</span></h2>
        <pre class="whitespace-pre text-green-300 bg-gray-900 p-2 rounded fade-in">
${JSON.stringify(data.ast, null, 2)}
        </pre>`;
            }

            if (analysisMode === "sem") {
                if (data.semantics && data.semantics.length > 0) {
                    outputDiv.innerHTML += `
            <hr class="section-divider">
            <h2 class='text-lg font-bold mt-4 text-red-400 flex items-center gap-2'>
    Errores Semánticos
    <span class="tooltip text-sm opacity-70" title="Errores como variables no declaradas, uso incorrecto de 'break' o 'return'">🛈</span>
</h2>

            <ul class="list-disc pl-5 text-red-400 space-y-1 fade-in">
                ${data.semantics.map(msg => `<li class="semantic-error-item">${msg}</li>`).join("")}
            </ul>`;
                } else {
                    outputDiv.innerHTML += `
            <hr class="section-divider"><h2 class='text-lg font-bold mt-4 text-green-400 fade-in'>Sin errores semánticos <span class="tooltip" title="El código no presenta errores semánticos">🛈</span></h2>`;
                }
            }



        } else {
            outputDiv.innerHTML =
                `<div class='text-red-500'>
               <h2 class='font-bold mb-1'>Ocurrió un error durante el análisis</h2>
               <p>${traducirError(data.error)}</p>
             </div>`;
        }
    } catch (err) {
        console.error(err);
        loadingDiv.classList.add("hidden");
        outputDiv.innerHTML =
            `<div class='text-red-500'>
             <h2 class='font-bold mb-1'>No se pudo conectar con el servidor</h2>
             <p>Revisa que el backend esté en ejecución en <code>localhost:5000</code> y que no existan bloqueos de red.</p>
           </div>`;
    }
}

document.getElementById("fileInput")
    .addEventListener("change", (evt) => {
        const file = evt.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (e) =>
            (document.getElementById("codeInput").value = e.target.result);
        reader.readAsText(file);
    });

function loadExample() {
    if (analysisMode === "asm") {
        const ejemplos = [
            `MOV A, 5
MOV B, 10
CMP A, B
JNE DIF
PRINT A
JMP END

DIF:
PRINT B

END:
HALT`,

            `MOV D, 3
MOV E, 4
ADD D, E
PRINT D
SUB D, E
PRINT D
MUL D, E
PRINT D
DIV D, E
PRINT D`,

            `MOV A, 6
MOV B, 3
AND A, B
PRINT A
NOT B
PRINT B`,

            `MOV HL, 1234
PRINT HL
MOV SP, 4096
PRINT SP`,

            `MOV C, 42
HALT
PRINT C`,

            `; Operación inválida esperada (para test de errores)
MOV A, BC`,

            `; Salto a etiqueta no existente
JMP NO_EXISTE`
        ];

        const random = Math.floor(Math.random() * ejemplos.length);
        document.getElementById("codeInput").value = ejemplos[random];
    } else {
        document.getElementById("codeInput").value =
            `def suma(a, b):
    return a + b

print(suma(5, 10))`;
    }
}



//Descomentar el de abajo si quieres ver la cara de Solano


particlesJS("particles-js",
    { "particles": { "number": { "value": 80, "density": { "enable": true, "value_area": 800 } }, "color": { "value": "#ffffff" }, "shape": { "type": "circle", "stroke": { "width": 0, "color": "#000000" }, "polygon": { "nb_sides": 5 }, "image": { "src": "img/github.svg", "width": 100, "height": 100 } }, "opacity": { "value": 0.5, "random": false, "anim": { "enable": false, "speed": 1, "opacity_min": 0.1, "sync": false } }, "size": { "value": 3, "random": true, "anim": { "enable": false, "speed": 40, "size_min": 0.1, "sync": false } }, "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.4, "width": 1 }, "move": { "enable": true, "speed": 6, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false, "attract": { "enable": false, "rotateX": 600, "rotateY": 1200 } } }, "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": true, "mode": "repulse" }, "onclick": { "enable": true, "mode": "push" }, "resize": true }, "modes": { "grab": { "distance": 400, "line_linked": { "opacity": 1 } }, "bubble": { "distance": 400, "size": 40, "duration": 2, "opacity": 8, "speed": 3 }, "repulse": { "distance": 200, "duration": 0.4 }, "push": { "particles_nb": 4 }, "remove": { "particles_nb": 2 } } }, "retina_detect": true }); var count_particles, stats, update; stats = new Stats; stats.setMode(0); stats.domElement.style.position = 'absolute'; stats.domElement.style.left = '0px'; stats.domElement.style.top = '0px'; document.body.appendChild(stats.domElement); count_particles = document.querySelector('.js-count-particles'); update = function () { stats.begin(); stats.end(); if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) { count_particles.innerText = window.pJSDom[0].pJS.particles.array.length; } requestAnimationFrame(update); }; requestAnimationFrame(update);;

/*

particlesJS("particles-js", {
    "particles": {
        "number": { "value": 30, "density": { "enable": true, "value_area": 800 } },
        "color": { "value": "#ffffff" },
        "shape": {
            "type": "image",
            "stroke": { "width": 0, "color": "#000000" },
            "polygon": { "nb_sides": 5 },
            "image": { "src": "./images/Solano.jpg", "width": 100, "height": 100 }
        },
        "opacity": { "value": 0.4, "random": true, "anim": { "enable": true, "speed": 1, "opacity_min": 0, "sync": false } },
        "size": { "value": 90, "random": true, "anim": { "enable": false, "speed": 0.2, "size_min": 0.3, "sync": false } },
        "line_linked": { "enable": true, "distance": 4.1, "color": "#ffffff", "opacity": 0.64, "width": 1 },
        "move": { "enable": true, "speed": 2.3, "direction": "none", "random": true, "straight": false, "out_mode": "out", "bounce": false }
    },
    "interactivity": {
        "detect_on": "canvas",
        "events": {
            "onhover": { "enable": true, "mode": "repulse" },
            "onclick": { "enable": true, "mode": "repulse" },
            "resize": true
        },
        "modes": {
            "grab": { "distance": 400, "line_linked": { "opacity": 1 } },
            "bubble": { "distance": 250, "size": 0, "duration": 2, "opacity": 0, "speed": 3 },
            "repulse": { "distance": 200, "duration": 0.2 },
            "push": { "particles_nb": 4 },
            "remove": { "particles_nb": 2 }
        }
    },
    "retina_detect": true
});
<<<<<<< HEAD
=======

>>>>>>> 8cb357c29b6e35da6380808f636ab612419bfbe9
*/