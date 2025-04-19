const API_URL = 'http://127.0.0.1:5000/book';

// Função que resgata os livros no banco e monta uma tabela com as informações
async function getAllBooks() {
    const request_response = await fetch(API_URL);
    const response = await request_response.json();
    const books = response.books

    const tabela = document.getElementById('book-table').getElementsByTagName('tbody')[0];
    tabela.innerHTML = '';

    books.forEach(book => {
        const row = tabela.insertRow();  // Cria uma nova linha

        // Cria as células para cada atributo
        const cellName = row.insertCell(0);
        const cellAuthor = row.insertCell(1);
        const cellGenre = row.insertCell(2);
        const cellNumPages = row.insertCell(3);
        const cellSynopsis = row.insertCell(4);
        const cellNote = row.insertCell(5)
        const cellCompleted = row.insertCell(6);
        const cellDelete = row.insertCell(7);

        // Preenche as células com os dados do livro
        cellName.textContent = book.name;
        cellAuthor.textContent = book.author;
        cellGenre.textContent = book.genre;
        cellNumPages.textContent = book.num_pages;
        cellSynopsis.textContent = book.des_synopsis || 'Não disponível';
        cellCompleted.textContent = book.flg_completed ? 'Sim' : 'Não';
        cellNote.textContent = book.des_observacao || 'Sem observação';

        // Adiciona o checkbox para deletar
        const checkbox = document.createElement('input');
        checkbox.name = 'flg_selected'
        checkbox.type = 'checkbox';
        checkbox.value = book.id;
        cellDelete.appendChild(checkbox);
    });
}

// Função para obter um livro da tabela de livros
async function getBookById() {
    const checkbox = document.querySelectorAll('input[name="flg_selected"]:checked');

    if (checkbox.length > 1) {
        alert("Selecione apenas um livro.");
        return;
    }

    const book_id = checkbox[0].value;
    //console.log(checkbox)

    const request_response = await fetch(`http://127.0.0.1:5000/book/${book_id}`);
    const response = await request_response.json();
    const book_data = response.book

    const form = document.getElementById('book-form');
    form.id.value = book_data.id
    console.log(form.id.value)
    form.name.value = book_data.name;
    form.author.value = book_data.author;
    form.genre.value = book_data.genre;
    form.num_pages.value = book_data.num_pages;
    form.des_synopsis.value = book_data.des_synopsis;
    form.des_note.value = book_data.des_observacao;
    form.flg_completed.checked = book_data.flg_completed;
}

// Função que realiza o cadastro de um novo livro 
async function createNewBook(e) {
    e.preventDefault();

    const form = e.target;
    const data = {
        name: form.name.value,
        author: form.author.value,
        genre: form.genre.value,
        num_pages: parseInt(form.num_pages.value),
        des_synopsis: form.des_synopsis.value,
        flg_completed: form.flg_completed.checked,
        des_observacao: form.des_note.value
    };

    await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });

    form.reset();
    getAllBooks();
}

// Função que realiza a atualização do cadastro de um livro
async function updateBook(e) {
    e.preventDefault();

    const form = document.getElementById('book-form');
    const book_id = form.id.value;
    const data = {
        name: form.name.value,
        author: form.author.value,
        genre: form.genre.value,
        num_pages: parseInt(form.num_pages.value),
        des_observacao: form.des_note.value,
        des_synopsis: form.des_synopsis.value,
        flg_completed: form.flg_completed.checked
    };

    await fetch(`${API_URL}/${book_id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        
        body: JSON.stringify(data)
    });

    form.reset();
    getAllBooks();
}

// Função que deleta os livros que foram selecionados 
async function deleteSelectedBooks() {
    const checkboxes = document.querySelectorAll('input[name="flg_selected"]:checked');

    const idsToDelete = [];
    checkboxes.forEach(checkbox => {
        idsToDelete.push(checkbox.value);  // Adiciona o ID do livro a ser deletado
    });

    // Envia os IDs para a API deletar
    if (idsToDelete.length > 0) {
        for (const id of idsToDelete) {
            await fetch(`http://127.0.0.1:5000/book/${id}`, {
                method: 'DELETE'
            });
        }

        // Recarrega os livros após a exclusão
        getAllBooks();
    } else {
        alert('Selecione ao menos um livro para deletar');
    }
}


document.getElementById('delete-selected').addEventListener('click', deleteSelectedBooks);
document.getElementById('search-selected').addEventListener('click', getBookById);

document.getElementById('book-form').addEventListener('submit', createNewBook);
document.getElementById('edit-btn').addEventListener('click', updateBook);

getAllBooks();