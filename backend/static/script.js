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