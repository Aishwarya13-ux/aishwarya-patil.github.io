document.addEventListener('DOMContentLoaded', function() {

    // --- tsParticles Configuration - Enhanced for Sparkle ---
    tsParticles.load("tsparticles", {
        fullScreen: {
            enable: true,
            zIndex: -1 // Keep behind content
        },
        particles: {
            number: {
                value: 250, // Increase particle count slightly
                density: {
                    enable: true,
                    value_area: 900
                }
            },
            color: {
                // Brighter, more varied colors for sparkle
                value: ["#FFFFFF", "#8A2BE2", "#c084fc", "#f0abfc", "#4F46E5"]
            },
            shape: {
                type: "circle", // Simple shape works well for stars/sparks
            },
            opacity: {
                value: { min: 0.1, max: 0.8 }, // Wider opacity range
                animation: {
                    enable: true,
                    speed: 5, // Faster flicker
                    minimumValue: 0.1,
                    sync: false
                }
            },
            size: {
                 value: { min: 1, max: 3 }, // Keep particles small
                 animation: { // Subtle pulsing size adds dynamism
                    enable: true,
                    speed: 4,
                    minimumValue: 0.5,
                    sync: false,
                    startValue: "random", // Start particles at random sizes within range
                    destroy: "none"
                }
            },
            links: {
                enable: false, // No lines connecting particles
            },
            move: {
                enable: true,
                speed: 1, // Slightly increased speed for more "life"
                direction: "none",
                random: true,
                straight: false, // Random paths
                outModes: {
                    default: "out"
                },
                attract: { // Keep disabled unless you want clumping
                    enable: false,
                    rotateX: 900,
                    rotateY: 1200
                },
            },
             twinkle: {
                particles: {
                    enable: true,
                    frequency: 0.05, // How often they twinkle
                    opacity: 1 // Twinkle affects opacity
                }
            }
        },
        interactivity: {
            detectsOn: "canvas",
            events: {
                onHover: {
                    enable: true,
                    mode: "repulse" // Pushing particles away adds interaction
                },
                onClick: {
                    enable: true,
                    mode: "push" // Adding particles on click
                },
                resize: true
            },
            modes: {
                repulse: {
                    distance: 100, // How far particles push away
                    duration: 0.4,
                    factor: 100, // Strength of repulsion
                    speed: 1,
                    maxSpeed: 50,
                    easing: "ease-out-quad"
                },
                push: {
                    quantity: 4
                },
            }
        },
        detectRetina: true // Keep for sharp particles on high-res screens
    });


    // --- Typing Effect ---
    const typingTextElement = document.querySelector('.typing-text');
    const words = ["Android Developer", "Web Developer", "Full Stack Developer", "UI/UX Designer", "Learner"];
    let wordIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingSpeed = 100;
    const deletingSpeed = 50;
    const delayBetweenWords = 1500;

    function type() {
        if (!typingTextElement) return;

        const currentWord = words[wordIndex];
        if (!currentWord) return;

        const isEndOfWord = !isDeleting && charIndex === currentWord.length;
        const isStartOfWord = isDeleting && charIndex === 0;

        if (isDeleting) {
            typingTextElement.textContent = currentWord.substring(0, charIndex - 1);
            charIndex--;
        } else {
            typingTextElement.textContent = currentWord.substring(0, charIndex + 1);
            charIndex++;
        }

        typingTextElement.style.borderRightColor = 'var(--primary-color)'; // Keep cursor visible

        let delta = typingSpeed;
        if (isDeleting) delta = deletingSpeed;

        if (isEndOfWord) {
            delta = delayBetweenWords;
            isDeleting = true;
        }

        if (isStartOfWord) {
            isDeleting = false;
            wordIndex = (wordIndex + 1) % words.length;
            // Optionally add a small pause before typing the next word
            delta = 500; // e.g., half-second pause
        }

        setTimeout(type, delta);
    }

    if (typingTextElement) {
        typingTextElement.textContent = ''; // Clear initial content
        setTimeout(type, delayBetweenWords / 2); // Start typing sooner
    }


    // --- Project Filtering ---
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');
    const projectsGrid = document.querySelector('.projects-grid'); // Get the grid container

    if(filterButtons.length > 0 && projectCards.length > 0 && projectsGrid) { // Check elements exist

        // Function to handle card visibility after transition
        const handleHideTransition = (event) => {
            if (event.propertyName === 'opacity' && event.target.classList.contains('hide')) {
                 event.target.style.display = 'none';
            }
        };

         // Attach transitionend listener to the grid container (event delegation)
         projectsGrid.addEventListener('transitionend', handleHideTransition);


        filterButtons.forEach(button => {
            button.addEventListener('click', () => {
                filterButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');

                const filterValue = button.getAttribute('data-filter');

                projectCards.forEach(card => {
                    const cardCategory = card.getAttribute('data-category');
                    const shouldShow = (filterValue === 'all' || filterValue === cardCategory);

                    if (shouldShow) {
                         // Make visible: remove 'hide' class first, then set display
                         card.classList.remove('hide');
                         card.style.display = 'flex'; // Or 'block'
                    } else {
                        // Hide: add 'hide' class to trigger CSS transition
                        card.classList.add('hide');
                        // display: none; will be handled by the transitionend listener
                    }
                });
            });
        });
    } // End check for filter buttons/cards/grid

}); // End of DOMContentLoaded
