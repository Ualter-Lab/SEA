const campoCurso = document.getElementById("curso");
const divSerie = document.getElementById("div_serie");
const divTurma = document.getElementById("div_turma");
const divMatricula = document.getElementById("div_matricula");

function gerenciarCampos() {
// Se não encontrar o campo do curso, interrompe a função para não dar erro
if (!campoCurso) return;

const éProfessor = campoCurso.value === "Professor";

// Gerencia a visibilidade das divs de forma limpa (se for professor, esconde)
divSerie?.classList.toggle("hidden", éProfessor);
divTurma?.classList.toggle("hidden", éProfessor);
divMatricula?.classList.toggle("hidden", éProfessor);

// Seleciona os elementos internos de forma segura usando o operador '?.'
const selectSerie = divSerie?.querySelector("select");
const selectTurma = divTurma?.querySelector("select");
const inputMatricula = divMatricula?.querySelector("input");

// Se o elemento existir, define o 'required' (oposto de éProfessor)
if (selectSerie) selectSerie.required = !éProfessor;
if (selectTurma) selectTurma.required = !éProfessor;
if (inputMatricula) inputMatricula.required = !éProfessor;
}

// Escuta a mudança no select
campoCurso.addEventListener("change", gerenciarCampos);

// Executa uma vez ao carregar a página para alinhar o estado inicial
document.addEventListener("DOMContentLoaded", gerenciarCampos);

function mostrarToast(mensagem, tipo = "sucesso") {
    const container = document.getElementById("toast-container");

    if (!container) {
        console.error("Container de notificações não encontrado!");
        return;
    }

    const estilos = {
        sucesso: "bg-green-600",
        erro: "bg-red-600",
        aviso: "bg-yellow-500"
    };

    const icones = {
        sucesso: "✓",
        erro: "✕",
        aviso: "!"
    };

    const toast = document.createElement("div");

    toast.className = `${estilos[tipo] || estilos.aviso} text-white px-5 py-3 rounded-xl shadow-lg flex items-center gap-3`;

    const icone = document.createElement("span");
    icone.textContent = icones[tipo] || "!";

    const texto = document.createElement("span");
    texto.textContent = mensagem;

    toast.append(icone, texto);
    container.appendChild(toast);

    setTimeout(() => toast.remove(), 3500);
}

toast.className = `${estilos[tipo] || estilos.aviso} border-0 text-white px-5 py-3 rounded-xl shadow-lg flex items-center gap-3`;