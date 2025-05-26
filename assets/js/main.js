/**
* Template Name: Vesperr - v4.10.0
* Template URL: https://bootstrapmade.com/vesperr-free-bootstrap-template/
* Author: BootstrapMade.com
* License: https://bootstrapmade.com/license/
*/
(function () {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    let selectEl = select(el, all)
    if (selectEl) {
      if (all) {
        selectEl.forEach(e => e.addEventListener(type, listener))
      } else {
        selectEl.addEventListener(type, listener)
      }
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Scrolls to an element with header offset
   */
  const scrollto = (el) => {
    let header = select('#header')
    let offset = header.offsetHeight

    if (!header.classList.contains('header-scrolled')) {
      offset -= 20
    }

    let elementPos = select(el).offsetTop
    window.scrollTo({
      top: elementPos - offset,
      behavior: 'smooth'
    })
  }

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Mobile nav toggle
   */
  on('click', '.mobile-nav-toggle', function (e) {
    select('#navbar').classList.toggle('navbar-mobile')
    this.classList.toggle('bi-list')
    this.classList.toggle('bi-x')
  })

  /**
   * Mobile nav dropdowns activate
   */
  on('click', '.navbar .dropdown > a', function (e) {
    if (select('#navbar').classList.contains('navbar-mobile')) {
      e.preventDefault()
      this.nextElementSibling.classList.toggle('dropdown-active')
    }
  }, true)

  /**
   * Scrool with ofset on links with a class name .scrollto
   */
  on('click', '.scrollto', function (e) {
    if (select(this.hash)) {
      e.preventDefault()

      let navbar = select('#navbar')
      if (navbar.classList.contains('navbar-mobile')) {
        navbar.classList.remove('navbar-mobile')
        let navbarToggle = select('.mobile-nav-toggle')
        navbarToggle.classList.toggle('bi-list')
        navbarToggle.classList.toggle('bi-x')
      }
      scrollto(this.hash)
    }
  }, true)

  /**
   * Scroll with ofset on page load with hash links in the url
   */
  window.addEventListener('load', () => {
    if (window.location.hash) {
      if (select(window.location.hash)) {
        scrollto(window.location.hash)
      }
    }
  });

  /**
   * Testimonials slider
   */
  new Swiper('.testimonials-slider', {
    speed: 600,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    slidesPerView: 'auto',
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    },
    breakpoints: {
      320: {
        slidesPerView: 1,
        spaceBetween: 20
      },

      1200: {
        slidesPerView: 2,
        spaceBetween: 20
      }
    }
  });

  /**
   * Porfolio isotope and filter
   */
  window.addEventListener('load', () => {
    let portfolioContainer = select('.portfolio-container');
    if (portfolioContainer) {
      let portfolioIsotope = new Isotope(portfolioContainer, {
        itemSelector: '.portfolio-item',
        layoutMode: 'fitRows'
      });

      let portfolioFilters = select('#portfolio-flters li', true);

      on('click', '#portfolio-flters li', function (e) {
        e.preventDefault();
        portfolioFilters.forEach(function (el) {
          el.classList.remove('filter-active');
        });
        this.classList.add('filter-active');

        portfolioIsotope.arrange({
          filter: this.getAttribute('data-filter')
        });
        portfolioIsotope.on('arrangeComplete', function () {
          AOS.refresh()
        });
      }, true);
    }

  });

  /**
   * Initiate portfolio lightbox 
   */
  const portfolioLightbox = GLightbox({
    selector: '.portfolio-lightbox'
  });

  /**
   * Portfolio details slider
   */
  new Swiper('.portfolio-details-slider', {
    speed: 400,
    loop: true,
    autoplay: {
      delay: 5000,
      disableOnInteraction: false
    },
    pagination: {
      el: '.swiper-pagination',
      type: 'bullets',
      clickable: true
    }
  });

  /**
   * Animation on scroll
   */
  window.addEventListener('load', () => {
    reveal(2000);
    AOS.init({
      duration: 1000,
      easing: 'ease-in-out',
      once: true,
      mirror: false
    })
  });

  /**
   * Initiate Pure Counter 
   */
  new PureCounter();

})()

/* --- Highlight animation --- */

$(window).scroll(function(){
  reveal(300);
  revealBG(300);
  revealBG_gray(300);
})

function reveal(delay) {
  var reveals = document.querySelectorAll('.underlined');
  let position = window.scrollY;
  for (var i = 0; i < reveals.length; i++) {
    var windowHeight = window.innerHeight;
    var elementTop = reveals[i].getBoundingClientRect().top;
    var elementVisible = 150;
    if (elementTop < windowHeight - elementVisible) {
      setTimeout((function(){
        this.classList.add('active');
      }).bind(reveals[i]), delay);
    } else {
      reveals[i].classList.remove('active');
    }
  }
}

function revealBG(delay) {
  var reveals = document.querySelectorAll('.underlined--bg');
  let position = window.scrollY;
  for (var i = 0; i < reveals.length; i++) {
    var windowHeight = window.innerHeight;
    var elementTop = reveals[i].getBoundingClientRect().top;
    var elementVisible = 150;
    if (elementTop < windowHeight - elementVisible) {
      setTimeout((function(){
        this.classList.add('active--bg');
      }).bind(reveals[i]), delay);
    } else {
      reveals[i].classList.remove('active--bg');
    }
  }
}

function showMashupViz(containerIdToShow) {
  document.querySelectorAll('.mashup-viz-container').forEach(div => div.style.display = 'none');
  const targetDiv = document.getElementById(containerIdToShow);
  if (targetDiv) {
    targetDiv.style.display = 'block';
    if (!targetDiv.dataset.rendered) {
      if (containerIdToShow === 'viz-mashup1-container') {
        window.renderMashup1('viz-mashup1-container');
      } else if (containerIdToShow === 'viz-mashup2-container') {
        window.renderMashup2('viz-mashup2-container');
      } else if (containerIdToShow === 'viz3_1-container') {
        window.renderViz3_1('viz3_1-container');
      } else if (containerIdToShow === 'viz4_map-container') {
        window.renderViz4_map('viz4_map-container');
      }
      // Mark as rendered
      targetDiv.dataset.rendered = "true";
    }
  }
}


function revealBG_gray(delay) {
  var reveals = document.querySelectorAll('.underlined--bg-g');
  let position = window.scrollY;
  for (var i = 0; i < reveals.length; i++) {
    var windowHeight = window.innerHeight;
    var elementTop = reveals[i].getBoundingClientRect().top;
    var elementVisible = 150;
    if (elementTop < windowHeight - elementVisible) {
      setTimeout((function(){
        this.classList.add('active--bg-g');
      }).bind(reveals[i]), delay);
    } else {
      reveals[i].classList.remove('active--bg-g');
    }
  }
}


function showMashupViz(id, btn) {
  document.querySelectorAll('.mashup-viz-container').forEach(el => el.style.display = 'none');
  document.getElementById(id).style.display = 'block';
  document.querySelectorAll('.btn-mashup').forEach(b => b.classList.remove('btn-mashup-active', 'active'));
  btn.classList.add('btn-mashup-active', 'active');

  // RENDER the appropriate visuals
  if (id === 'viz-mashup1-container') {
    showMashup1Tab('map', document.querySelector('.btn-mashup1-viz'));
  } else if (id === 'viz-mashup2-container') {
    showMashup2Year(2017, document.querySelector('#viz2-year-buttons .btn-mashup-year'));
  } else if (id === 'viz3_1-container') {
    if (window.renderViz3_1) window.renderViz3_1("viz3_1-container");
  } else if (id === 'viz4_map-container') {
    if (window.renderViz4_map) window.renderViz4_map("viz4_map-container");
  }
}

function showMashup1Tab(tab, btn) {
  // Tab highlight
  document.querySelectorAll('.btn-mashup1-tab').forEach(b => b.classList.remove('btn-mashup-active', 'active'));
  if (btn) btn.classList.add('btn-mashup-active', 'active');

  // Hide all
  document.getElementById('mashup1-map-pane').style.display = 'none';
  document.getElementById('mashup1-correlation-img').style.display = 'none';
  document.getElementById('mashup1-regression-img').style.display = 'none';

  // Show selected
  if (tab === 'map') {
    document.getElementById('mashup1-map-pane').style.display = 'block';
  } else if (tab === 'correlation') {
    document.getElementById('mashup1-correlation-img').style.display = 'block';
  } else if (tab === 'regression') {
    document.getElementById('mashup1-regression-img').style.display = 'block';
  }
}

function setMashup1MapYear(year, btn) {
  // Year button highlight (only in map pane)
  document.querySelectorAll('#viz1-year-buttons .btn-mashup-year').forEach(b => b.classList.remove('btn-mashup-active', 'active'));
  if (btn) btn.classList.add('btn-mashup-active', 'active');
  // Set iframe src
  document.getElementById('mashup1iframe').src = 'visualizations/viz1_map_NO2_' + year + '.html';
}


function setMashup2Year(year, button) {
  document.getElementById("mashup2-scatter").src = `visualizations/viz2_scatter${year}.html`;
  document.getElementById("mashup2-bar").src = `visualizations/viz2_bar_chart_country_${year}.html`;

  const buttons = document.querySelectorAll("#viz2-year-buttons .btn-mashup-year");
  buttons.forEach(btn => {
    btn.classList.remove("active");
    btn.classList.remove("btn-mashup-active");
  });

  button.classList.add("active");
  button.classList.add("btn-mashup-active");

  button.blur(); // opzionale, aiuta con :focus
}
