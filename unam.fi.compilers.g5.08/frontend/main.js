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

        updateParticlesColor(mode);
    }

    document.querySelectorAll(".mode-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            analysisMode = btn.dataset.mode;

            // Resetear estilos de todos los botones
            document.querySelectorAll(".mode-btn").forEach(b => {
                b.classList.remove(
                    "ring-2",
                    "ring-blue-500",
                    "text-blue-500",
                    "text-blue-600",
                    "dark:text-blue-400",
                    "bg-white",
                    "bg-gray-900",
                    "dark:bg-gray-900",
                    "bg-blue-100",
                    "dark:bg-gray-800"
                );
            });

            // Estilo activo al botón seleccionado
            btn.classList.add(
                "ring-2",
                "ring-blue-500",
                "text-blue-600",
                "dark:text-blue-400",
                "bg-blue-100",
                "dark:bg-gray-800"
            );

            // Limpia resultados anteriores
            document.getElementById("output").innerHTML = "";
        });
    });

    applyTheme(localStorage.getItem('theme') || 'dark');

    // Alterna entre claro y oscuro al hacer clic
    themeBtn.addEventListener('click', () => {
        const currentTheme = localStorage.getItem('theme');
        applyTheme(currentTheme === 'dark' ? 'light' : 'dark');

        // Mostrar confirmación visual
        const msg = document.createElement('div');
        msg.textContent = "¡Tema cambiado!";
        msg.className = "fixed top-5 right-5 px-4 py-2 rounded bg-green-600 text-white shadow-lg z-50 animate-bounce";
        document.body.appendChild(msg);

        setTimeout(() => msg.remove(), 1500);

        const oldMsg = document.getElementById("theme-msg");
        if (oldMsg) oldMsg.remove();
        msg.id = "theme-msg";

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

function updateParticlesColor(theme) {
    const color = theme === 'dark' ? '#ffffff' : '#1f2937'; // blanco u oscuro
    if (window.pJSDom && window.pJSDom.length > 0) {
        const pJS = window.pJSDom[0].pJS;
        pJS.particles.color.value = color;
        pJS.particles.line_linked.color = color;
        pJS.fn.particlesRefresh();
    }
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

        if (!resp.ok) {
            outputDiv.innerHTML =
                `<div class='text-red-500'>
           <h2 class='font-bold mb-1'>Ocurrió un error durante el análisis</h2>
           <p>${traducirError(data.error)}</p>
         </div>`;
            return;  // <- ¡IMPORTANTE!
        }

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
      <span class="tooltip text-sm opacity-70"
            title="Errores como variables no declaradas, uso incorrecto de 'break' o 'return'">🛈</span>
    </h2>
    <ul class="list-disc pl-5 text-red-400 space-y-1 fade-in">
      ${data.semantics.map(msg => `<li>${msg}</li>`).join("")}
    </ul>`;
                } else {
                    outputDiv.innerHTML += `
    <hr class="section-divider"><h2 class='text-lg font-bold mt-4 text-center text-green-400 fade-in'>Sin errores semánticos <span class="tooltip" title="El código no presenta errores semánticos">🛈</span></h2>`;
                }

                // 🔽 Mostrar SIEMPRE la salida si la clave existe
                if ("output" in data) {
                    const outText = Array.isArray(data.output)
                        ? data.output.join("\n")
                        : String(data.output);
                    outputDiv.innerHTML += `<h2 class='text-lg font-bold mt-4 text-blue-300'>Salida del programa:</h2>
<pre class="bg-gray-900 text-yellow-300 p-2 rounded">
${outText || "(el programa no produjo salida)"}
    </pre>`;
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
    const ejemplosAsm = [
        { titulo: "Comparación y salto condicional", codigo: `MOV A, 5\nMOV B, 10\nCMP A, B\nJNE DIF\nPRINT A\nJMP END\n\nDIF:\nPRINT B\n\nEND:\nHALT` },
        { titulo: "Aritmética: ADD, SUB, MUL, DIV", codigo: `MOV D, 3\nMOV E, 4\nADD D, E\nPRINT D\nSUB D, E\nPRINT D\nMUL D, E\nPRINT D\nDIV D, E\nPRINT D` },
        { titulo: "Operadores lógicos: AND y NOT", codigo: `MOV A, 6\nMOV B, 3\nAND A, B\nPRINT A\nNOT B\nPRINT B` },
        { titulo: "Registros HL y SP", codigo: `MOV HL, 1234\nPRINT HL\nMOV SP, 4096\nPRINT SP` },
        { titulo: "HALT con código posterior", codigo: `MOV C, 42\nHALT\nPRINT C` },
        { titulo: "Error: operación inválida", codigo: `; Operación inválida esperada (para test de errores)\nMOV A, BC` },
        { titulo: "Error: salto a etiqueta no existente", codigo: `; Salto a etiqueta no existente\nJMP NO_EXISTE` }
    ];

    const ejemplosPy = [
        { titulo: "Condicional if-elif-else", codigo: `edad = 18\n\nnota = 7\n\nif nota >= 9:\n    print("Excelente")\nelif nota >= 6:\n    print("Aprobado. Apruebeme Rene con 10 por fa")\nelse:\n    print("Reprobado")` },
        { titulo: "Condicional con and", codigo: `edad = 20\ntiene_ine = True\n\nif edad >= 18 and tiene_ine:\n    print("Puedes votar")` },
        { titulo: "Bucle while", codigo: `contador = 1\nwhile contador <= 5:\n    print("Contando:",contador")\n    contador += 1` },
        { titulo: "Lista + for + append", codigo: `frutas = ["manzana", "banana", "cereza"]\nfrutas.append("naranja")\n\nfor fruta in frutas:\n    print(fruta)` },
        { titulo: "Uso de len()", codigo: `colores = ["rojo", "azul", "verde"]\nprint("Número de colores:", len(colores))\nprint(colores)` },
        { titulo: "Función que suma 1", codigo: `def sumar(a):\n    return a + 1` },
        { titulo: "Asignación y suma", codigo: `x = 5\ny = x + 2\n\nprint(x)\nprint(y)` }
    ];

    const modal = document.getElementById("exampleModal");
    const content = document.getElementById("exampleContent");
    const optionsContainer = document.getElementById("exampleOptions");
    const closeModalBtn = document.getElementById("closeModal");

    // Limpiar opciones previas
    optionsContainer.innerHTML = "";

    const ejemplos = analysisMode === "asm" ? ejemplosAsm : ejemplosPy;

    ejemplos.forEach((ejemplo, index) => {
        const btn = document.createElement("button");
        btn.className = "px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded text-left w-full transition-all duration-200";
        btn.textContent = `${index + 1}. ${ejemplo.titulo}`;
        btn.addEventListener("click", () => {
            document.getElementById("codeInput").value = ejemplo.codigo;
            modal.classList.add("hidden");
            modal.classList.remove("show");
        });
        optionsContainer.appendChild(btn);
    });

    // Mostrar modal con animación
    modal.classList.remove("hidden");
    setTimeout(() => modal.classList.add("show"), 10); // retraso para permitir transición

    // Cerrar modal
    closeModalBtn.onclick = () => {
        modal.classList.remove("show");
        setTimeout(() => modal.classList.add("hidden"), 300); // espera a que termine la animación
    };
}

// Estas son las partículas para que se vea más agradable y tenga vida la página
particlesJS("particles-js",
    { "particles": { "number": { "value": 80, "density": { "enable": true, "value_area": 800 } }, "color": { "value": "#ffffff" }, "shape": { "type": "circle", "stroke": { "width": 0, "color": "#000000" }, "polygon": { "nb_sides": 5 }, "image": { "src": "img/github.svg", "width": 100, "height": 100 } }, "opacity": { "value": 0.5, "random": false, "anim": { "enable": false, "speed": 1, "opacity_min": 0.1, "sync": false } }, "size": { "value": 3, "random": true, "anim": { "enable": false, "speed": 40, "size_min": 0.1, "sync": false } }, "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.4, "width": 1 }, "move": { "enable": true, "speed": 6, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false, "attract": { "enable": false, "rotateX": 600, "rotateY": 1200 } } }, "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": true, "mode": "repulse" }, "onclick": { "enable": true, "mode": "push" }, "resize": true }, "modes": { "grab": { "distance": 400, "line_linked": { "opacity": 1 } }, "bubble": { "distance": 400, "size": 40, "duration": 2, "opacity": 8, "speed": 3 }, "repulse": { "distance": 200, "duration": 0.4 }, "push": { "particles_nb": 4 }, "remove": { "particles_nb": 2 } } }, "retina_detect": true }); var count_particles, stats, update; stats = new Stats; stats.setMode(0); stats.domElement.style.position = 'absolute'; stats.domElement.style.left = '0px'; stats.domElement.style.top = '0px'; document.body.appendChild(stats.domElement); count_particles = document.querySelector('.js-count-particles'); update = function () { stats.begin(); stats.end(); if (window.pJSDom[0].pJS.particles && window.pJSDom[0].pJS.particles.array) { count_particles.innerText = window.pJSDom[0].pJS.particles.array.length; } requestAnimationFrame(update); }; requestAnimationFrame(update);;
