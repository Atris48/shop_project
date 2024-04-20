document.addEventListener("DOMContentLoaded", function () {
  // Scroll Top Function Start
  const scrollTopFooter = document.getElementById("scroll-top-button-footer");
  if (scrollTopFooter)
    scrollTopFooter.addEventListener("click", () =>
      window.scrollTo({ top: 0, behavior: "smooth" }),
    );

  // Scroll Top Function End

  // Theme Section Start
  const theme = {
    current: localStorage.getItem("theme"),
    toggleDesktop: document.getElementById("toggleThemeDesktop"),
    toggleMobile: document.getElementById("toggleThemeMobile"),
    iconDesktop: document.getElementById("themeIconDesktop"),
    iconMobile: document.getElementById("themeIconMobile"),
    text: document.getElementById("themeText"),
  };

  const setThemeInfo = (mode) => {
    const isDark = mode === "dark";
    if (!theme.iconDesktop || !theme.iconMobile) return;
    theme.iconDesktop.innerHTML =
      theme.iconMobile.innerHTML = `<use xlink:href="#${
        isDark ? "sun" : "moon"
      }" />`;
    theme.text.innerHTML = `حالت ${isDark ? "شب" : "روز"}`;
  };

  setThemeInfo(theme.current);

  const toggleTheme = () => {
    const isDarkMode = document.documentElement.classList.toggle("dark");
    setThemeInfo(isDarkMode ? "dark" : "light");
    localStorage.setItem("theme", isDarkMode ? "dark" : "light");
  };
  const isDark = () => {
    return document.documentElement.classList.contains("dark");
  };

  const isAppearanceTransition =
    typeof document !== "undefined" &&
    document.startViewTransition &&
    !window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function toggleDark(event) {
    if (!isAppearanceTransition || !event) {
      toggleTheme();
      return;
    }

    const x = event.clientX;
    const y = event.clientY;
    const endRadius = Math.hypot(
      Math.max(x, innerWidth - x),
      Math.max(y, innerHeight - y),
    );

    const transition = document.startViewTransition(async () => {
      toggleTheme();
    });

    transition.ready.then(() => {
      const clipPath = [
        `circle(0px at ${x}px ${y}px)`,
        `circle(${endRadius}px at ${x}px ${y}px)`,
      ];
      document.documentElement.animate(
        {
          clipPath: isDark() ? [...clipPath].reverse() : clipPath,
        },
        {
          duration: 500,
          easing: "ease-in",
          pseudoElement: isDark()
            ? "::view-transition-old(root)"
            : "::view-transition-new(root)",
        },
      );
    });
  }

  if (!theme.toggleDesktop || !theme.toggleMobile) return;
  else {
    theme.toggleDesktop.addEventListener("click", toggleDark);
    theme.toggleMobile.addEventListener("click", toggleDark);
  }
 

  // Theme Section End

  // Header Scripts Section Start

  // Toggle Desktop Mega menu ( Categories )
  const desktopMegamenuWrapper = document.getElementById(
    "desktopMegamenuWrapper",
  );
  const desktopMegamenu = document.getElementById("desktopMegamenu");
  const headerOverlay = document.getElementById("header-overlay");

  let showDesktopMegamenu = false;

  const toggleMegamenu = (event) => {
    showDesktopMegamenu = event.type === "mouseenter";
    desktopMegamenu.classList.toggle("hidden", !showDesktopMegamenu);
    headerOverlay.classList.toggle("hidden", !showDesktopMegamenu);
  };

  desktopMegamenuWrapper.addEventListener("mouseenter", toggleMegamenu);
  desktopMegamenuWrapper.addEventListener("mouseleave", toggleMegamenu);

  // Hide mobile navbar on Scroll Start
  let isSearchResultShow= false
  const mobileHeaderBottom = document.getElementById("mobile-header-bottom");
  const desktopHeaderBottom = document.getElementById("desktop-header-bottom");
  let isScrollingDown = false;
  let prevScrollPos = window.pageYOffset || document.documentElement.scrollTop;


  const handleScroll = () => {
    const currentScrollPos =
      window.pageYOffset || document.documentElement.scrollTop;

    if (currentScrollPos > 0 && currentScrollPos > prevScrollPos) {
      if (!isScrollingDown && !showDesktopMegamenu && !isSearchResultShow) {
        mobileHeaderBottom.classList.add("-translate-y-full");
        desktopHeaderBottom.classList.add("-translate-y-full");
        isScrollingDown = true;
      }
    } else {
      mobileHeaderBottom.classList.remove("-translate-y-full");
      desktopHeaderBottom.classList.remove("-translate-y-full");
      isScrollingDown = false;
    }

    prevScrollPos = currentScrollPos;
  };

  window.addEventListener("scroll", handleScroll);
  // Hide mobile navbar on Scroll End

  // Desktop Header Megamenu section
  const categoriesParentsMegamenu = document.querySelectorAll(
    "#mega-menu-parents li a",
  );
  const categoriesChildsMegamenu = document.querySelectorAll(
    "#mega-menu-childs > div[data-category-child]",
  );

  // Apply the classes to the first item at page load
  categoriesParentsMegamenu[0].classList.add("mega-menu-active");
  categoriesChildsMegamenu[0].classList.remove("hidden");

  categoriesParentsMegamenu.forEach((item) => {
    item.addEventListener("mouseenter", () => {
      // Remove the 'active' class from all parent categories and hide all child divs
      categoriesParentsMegamenu.forEach((otherItem) =>
        otherItem.classList.remove("mega-menu-active"),
      );
      categoriesChildsMegamenu.forEach((childDiv) =>
        childDiv.classList.add("hidden"),
      );

      // Add the 'active' class to the current parent category and show the corresponding child div
      item.classList.add("mega-menu-active");
      document
        .querySelector(
          `div[data-category-child="${item.getAttribute(
            "data-category-parent",
          )}"]`,
        )
        .classList.remove("hidden");
    });
  });
  // Header Scripts Section End

  new Swiper(".banner-slider", {
    pagination: {
      el: ".swiper-pagination",
      dynamicBullets: true,
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
    loop: true,
    autoplay: {
      delay: 3000,
    },
  });

  new Swiper(".product-slider", {
    slidesPerView: 1.5,
    spaceBetween: 14,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 2.5,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 3.5,
        spaceBetween: 10,
      },
      1024: {
        slidesPerView: 4.5,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 6,
        spaceBetween: 10,
      },
    },
  });
  new Swiper(".product-slider-wrapped", {
    slidesPerView: 1.7,
    spaceBetween: 2,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 2,
        spaceBetween: 2,
      },
      460: {
        slidesPerView: 2.5,
        spaceBetween: 2,
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 2,
      },
      768: {
        slidesPerView: 3.5,
        spaceBetween: 2,
      },
      1024: {
        slidesPerView: 4.5,
        spaceBetween: 2,
      },
      1380: {
        slidesPerView: 6,
        spaceBetween: 2,
      },
    },
  });
  new Swiper(".product-image-mobile-swiper", {
    pagination: {
      el: ".swiper-pagination",
    },
  });
  const product_gallery_image_desktop2 = new Swiper(
    ".product-image-desktop-2-swiper",
    {
      slidesPerView: 8,
      spaceBetween: 20,
      navigation: {
        nextEl: ".swiper-button-next",
        prevEl: ".swiper-button-prev",
      },
    },
  );
  new Swiper(".product-image-desktop-swiper", {
    thumbs: {
      swiper: product_gallery_image_desktop2,
      slideThumbActiveClass: "swiper-thumb-active",
    },
    pagination: {
      el: ".swiper-pagination",
    },
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },
  });

  new Swiper(".product-comments-swiper", {
    slidesPerView: 1.1,
    spaceBetween: 10,
    freeMode: true,

    breakpoints: {
      360: {
        slidesPerView: 1.2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 1.6,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
    },
  });
  new Swiper(".orders-product-swiper", {
    slidesPerView: 1.1,
    spaceBetween: 10,
    freeMode: true,

    breakpoints: {
      360: {
        slidesPerView: 1.2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 1.6,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 3.1,
        spaceBetween: 10,
      },
    },
  });
  new Swiper(".notifications-product-swiper", {
    slidesPerView: 1.1,
    spaceBetween: 10,
    freeMode: true,

    breakpoints: {
      360: {
        slidesPerView: 1.2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 1.6,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 3.1,
        spaceBetween: 10,
      },
    },
  });

  new Swiper(".blog-slider", {
    slidesPerView: 1.7,
    spaceBetween: 14,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 2,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 2.5,
        spaceBetween: 15,
      },
      640: {
        slidesPerView: 3,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 3.2,
        spaceBetween: 15,
      },
      1024: {
        slidesPerView: 4,
        spaceBetween: 20,
      },
      1380: {
        slidesPerView: 4,
        spaceBetween: 20,
      },
    },
  });
  new Swiper(".search-result-desktop", {
    slidesPerView: 1.3,
    spaceBetween: 10,
    freeMode: true,
    navigation: {
      nextEl: ".swiper-button-next",
      prevEl: ".swiper-button-prev",
    },

    breakpoints: {
      360: {
        slidesPerView: 1.5,
        spaceBetween: 10,
      },
      460: {
        slidesPerView: 2.1,
        spaceBetween: 10,
      },
      640: {
        slidesPerView: 2.5,
        spaceBetween: 10,
      },
      768: {
        slidesPerView: 2.1,
        spaceBetween: 10,
      },
      1024: {
        slidesPerView: 2.2,
        spaceBetween: 10,
      },
      1380: {
        slidesPerView: 2.5,
        spaceBetween: 10,
      },
    },
  });
  // Border Animation Section Start
  const setMousePosition = (e) => {
    document.querySelectorAll(".border-gradient").forEach((item) => {
      const { left, top } = item.getBoundingClientRect();
      const { clientX, clientY } = e;
      item.style.setProperty("--x", `${clientX - left}px`);
      item.style.setProperty("--y", `${clientY - top}px`);
    });
  };

  document.addEventListener("mousemove", setMousePosition);

  // Border Animation Section End

  // noUiSlider Section Start

  const shopPriceSlider = document.querySelectorAll("#shop-price-slider");
  const shopPriceSliderMin = document.querySelectorAll(
      "#shop-price-slider-min",
    ),
    shopPriceSliderMax = document.querySelectorAll("#shop-price-slider-max");

  shopPriceSlider.forEach((item) => {
    noUiSlider.create(item, {
      cssPrefix: "range-slider-",
      start: [0, 100_000_000],
      direction: "rtl",
      margin: 1,
      range: {
        min: 0,
        max: 100_000_000,
      },
      format: {
        to: function (value) {
          return value.toLocaleString("en-US", {
            style: "decimal",
            maximumFractionDigits: 0,
          });
        },
        from: function (value) {
          return parseFloat(value.replace(/,/g, ""));
        },
      },
    });

    item.noUiSlider.on("update", function (values, handle) {
      if (handle) {
        shopPriceSliderMax.forEach((price_item) => {
          price_item.innerHTML = values[handle];
        });
      } else {
        shopPriceSliderMin.forEach((price_item) => {
          price_item.innerHTML = values[handle];
        });
      }
    });
  });
  // noUiSlider Section End

  // Header Search Overlay Start
  function initializeSearchComponent(baseId, wrapperId, searchId, resultId) {
    const base = document.getElementById(baseId);
    const wrapper = document.getElementById(wrapperId);
    const search = document.getElementById(searchId);
    const result = document.getElementById(resultId);

    function hideSearchResults() {
      wrapper.classList.remove(
        "border",
        "bg-white",
        "dark:bg-zinc-900",
        "rounded-b-none",
      );
      wrapper.classList.add("bg-gray-100", "dark:bg-black");
      search.classList.remove("bg-white", "dark:bg-zinc-900");
      search.classList.add("bg-gray-100", "dark:bg-black");
      wrapper.classList.remove("rounded-b-none");
      headerOverlay.classList.add("hidden");
      result.classList.add("hidden");
      isSearchResultShow = false
    }

    search.addEventListener("focus", () => {
      wrapper.classList.add(
        "border",
        "bg-white",
        "dark:bg-zinc-900",
        "rounded-b-none",
      );
      wrapper.classList.remove("bg-gray-100", "dark:bg-black");
      search.classList.add("bg-white", "dark:bg-zinc-900");
      search.classList.remove("bg-gray-100", "dark:bg-black");
      headerOverlay.classList.remove("hidden");
      result.classList.remove("hidden");
      isSearchResultShow = true

    });

    return { base, hideSearchResults };
  }

  const { base: desktopBase, hideSearchResults: hideDesktopSearchResults } =
    initializeSearchComponent(
      "desktopHeaderSearchBase",
      "desktopHeaderSearchWrapper",
      "desktopHeaderSearch",
      "desktopHeaderSearchResult",
    );

  const { base: mobileBase, hideSearchResults: hideMobileSearchResults } =
    initializeSearchComponent(
      "mobileHeaderSearchBase",
      "mobileHeaderSearchWrapper",
      "mobileHeaderSearch",
      "mobileHeaderSearchResult",
    );

  // Add click event listener to the document
  document.addEventListener("mousedown", (event) => {
    if (
      !desktopBase.contains(event.target) &&
      !mobileBase.contains(event.target)
    ) {
      hideDesktopSearchResults();
      hideMobileSearchResults();
    }
  });

  // Header Search Overlay End
});
