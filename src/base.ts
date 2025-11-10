import 'flowbite';

export interface HTMXEventDetail {
  xhr: XMLHttpRequest;
  target: HTMLElement;
}

const themeToggleDarkIcons = document.querySelectorAll(
  '#theme-toggle-dark-icon',
);
const themeToggleLightIcons = document.querySelectorAll(
  '#theme-toggle-light-icon',
);

// Change the icons inside the button based on previous settings
if (
  localStorage.getItem('color-theme') === 'dark' ||
  (!('color-theme' in localStorage) &&
    window.matchMedia('(prefers-color-scheme: dark)').matches)
) {
  themeToggleLightIcons.forEach(function (el) {
    el.classList.remove('hidden');
  });
  document.documentElement.classList.add('dark');
} else {
  themeToggleDarkIcons.forEach(function (el) {
    el.classList.remove('hidden');
  });
  document.documentElement.classList.remove('dark');
}

const themeToggleButtons = document.querySelectorAll('#theme-toggle');

const docListItems = document.querySelectorAll('.doc-list-item') as NodeListOf<HTMLElement>;
function setCardBackground(item: HTMLElement, className: string): void {
  docListItems.forEach((el: Element) => el.classList.remove('bg-blue-200'));
  docListItems.forEach((el: Element) => el.classList.remove('bg-gray-800'));
  item.classList.add(className);
}

themeToggleButtons.forEach(function (themeToggleBtn) {
  themeToggleBtn.addEventListener('click', function () {
    // toggle icons inside button
    themeToggleDarkIcons.forEach(function (themeToggleDarkIcon) {
      themeToggleDarkIcon.classList.toggle('hidden');
    });

    themeToggleLightIcons.forEach(function (themeToggleLightIcon) {
      themeToggleLightIcon.classList.toggle('hidden');
    });

    // if set via local storage previously
    if (localStorage.getItem('color-theme')) {
      if (localStorage.getItem('color-theme') === 'light') {
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
        const selectedCard = document.querySelector('.doc-list-item.bg-blue-200') as HTMLElement;
        console.log(selectedCard);
        console.log("localStorage.getItem('color-theme') === 'light'", "setting bg-gray-800");
        setCardBackground(selectedCard, 'bg-gray-800');
      } else {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('color-theme', 'light');
        const selectedCard = document.querySelector('.doc-list-item.bg-gray-800') as HTMLElement;
        console.log(selectedCard);
        console.log("localStorage.getItem('color-theme') === 'dark'", "setting bg-blue-200");
        setCardBackground(selectedCard, 'bg-blue-200');
      }

      // if NOT set via local storage previously
    } else {
      if (document.documentElement.classList.contains('dark')) {
        document.documentElement.classList.remove('dark');
        localStorage.setItem('color-theme', 'light');
        const selectedCard = document.querySelector('.doc-list-item.bg-gray-800') as HTMLElement;
        console.log(selectedCard);
        console.log("document.documentElement.classList.contains('dark')", "setting bg-blue-200");
        setCardBackground(selectedCard, 'bg-blue-200');
      } else {
        document.documentElement.classList.add('dark');
        localStorage.setItem('color-theme', 'dark');
        const selectedCard = document.querySelector('.doc-list-item.bg-blue-200') as HTMLElement;
        console.log(selectedCard);
        console.log("document.documentElement.classList.contains('light')", "setting bg-gray-800");
        setCardBackground(selectedCard, 'bg-gray-800');
      }
    }
  });
});

const menuButton = document.querySelector("#dropdown-menu-button");
const menu = document.querySelector("#dropdown-menu");

menuButton.addEventListener("click", function () {
  menu.classList.toggle("hidden");
});


docListItems.forEach(item => {
  item.addEventListener('click', function () {
    const isDark = document.documentElement.classList.contains('dark');
    if (isDark) {
      setCardBackground(item, 'bg-gray-800');
    } else {
      setCardBackground(item, 'bg-blue-200');
    }
  });
});
