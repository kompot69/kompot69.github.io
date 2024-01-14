const illustrationsUrl = 'https://api.github.com/repos/kompot69/kompot69.github.io/contents/hornyshon/resume/img/illustration';
const comicUrl = 'https://api.github.com/repos/kompot69/kompot69.github.io/contents/hornyshon/resume/img/comic';

async function load_illustrations() {
    await fetch(illustrationsUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевой ответ не был успешным');
            }
            return response.json();
        })
        .then(illustrations => {
            const illustrationsView = document.getElementById("illustrations");
            for (let illustration of illustrations) {
                let img = document.createElement("img");
                img.src = "img/illustration/" + illustration.name;
                illustrationsView.appendChild(img);
            }
        })
        .catch(error => {
            console.error('Не удалось загрузить иллюстрации:', error);
        });
}

async function load_comic() {
    await fetch(comicUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Сетевой ответ не был успешным');
            }
            return response.json();
        })
        .then(comics => {
            const comicsView = document.getElementById("comics");
            for (let comic of comics) {
                let img = document.createElement("img");
                img.src = "img/comic/" + comic.name;
                comicsView.appendChild(img);
            }
        })
        .catch(error => {
            console.error('Не удалось загрузить комиксы:', error);
        });
}

function main() {
    load_illustrations();
    load_comic();
}

document.addEventListener('DOMContentLoaded', (event) => {
    const imgElement = document.getElementsByTagName('img');
    imgElement.addEventListener('click', () => {
        imgElement.style.height = '250px';
        document.body.style.margin = '0';
    });
});
