#!/cise/homes/luke.morris/local/bin/racket

#lang racket/base

#|
Author: Luke Lawlor Morris
This CGI is meant to keep track of multiphysics simulations in a leader-board format.
|#

(require
  net/cgi
  racket/date
  racket/format
  racket/vector
  scribble/html
  syntax/to-string)

;; Boilerplate for evals.
(define-namespace-anchor ns-a)
(define ns (namespace-anchor->namespace ns-a))

#| Database of records, plots, and diagrams |#
(struct record   (day-code initials multiphysics link dev-time fnote))
(struct picture  (title src alt width))
(struct scenario (name #|Relations:|# has-plot has-diagram))

(define (m-record day-code initials multiphysics link dev-time #:fnote [fnote ""])
  (record day-code initials multiphysics link dev-time fnote))
(define (m-picture title src alt #:width [width "300px"])
  (picture title src alt width))
(define (m-string-diagram title src #:width [width "300px"])
  (picture title src "A string diagram" width))
(define (m-scenario name has-plot has-diagram)
  (scenario name has-plot has-diagram))

(define records
  (list
   (m-record '(10 3 2022) "AB" "Navier-Stokes" "https://github.com/AlgebraicJulia/DECAPODES-Benchmarks" "18 months" #:fnote "Honorary permanent number one")
   (m-record '(24 4 2024) "GR" "Cahn-Hilliard" "https://algebraicjulia.github.io/Decapodes.jl/dev/ch/cahn-hilliard/" "10 minutes")
   (m-record '(21 7 2023) "GR" "Teacup Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/chemistry/brusselator_teapot.jl#L177" "15 minutes" #:fnote "Extending a simulation from the unit square to the unit sphere")
   (m-record '(7  4 2023) "LM" "Gray-Scott" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/chemistry/gray_scott.jl" "15 minutes")
   (m-record '(17 2 2023) "GR" "Icosphere-Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/367aad9c8fd4e725a97cd9ad074c5a7dd32711b2/examples/chemistry/brusselator.jl#L137" "15 minutes" #:fnote "Extending a simulation from the unit square to the unit sphere")
   (m-record '(1  9 2023) "LM & GR" "Burgers'" "https://github.com/AlgebraicJulia/Decapodes.jl/pull/145" "30 minutes")
   (m-record '(12 7 2023) "LM" "Halfar" "https://algebraicjulia.github.io/Decapodes.jl/dev/cism/cism/" "2 hours")
   (m-record '(11 7 2023) "LM" "Budyko-Sellers" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/climate/budyko_sellers.jl" "2 hours")
   (m-record '(16 2 2023) "LM & GR" "Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/brusselator/brusselator.jl" "2 hours")
   (m-record '(17 5 2024) "LM" "Navier-Stokes, Vorticity" "https://algebraicjulia.github.io/Decapodes.jl/dev/navier_stokes/ns/" "2 hours")
   (m-record '(13 7 2023) "LM" "Nonhydrostatic Buoyant Seawater" "https://algebraicjulia.github.io/Decapodes.jl/dev/nhs/nhs_lite" "4 hours")
   (m-record '(7  2 2023) "LM & JC & JG" "Multispecies Navier-Stokes" "https://github.com/AlgebraicJulia/Decapodes.jl/issues/70#issuecomment-1421598346" "5 hours" #:fnote "Starting from pre-formulated Navier-Stokes Decapode")
   (m-record '(9  5 2024) "LM" "Vorticity Navier-Stokes" "https://algebraicjulia.github.io/Decapodes.jl/dev/navier_stokes/ns/" "-")
   (m-record '(13 1 2025) "GR" "Porous Convection" "https://github.com/AlgebraicJulia/Decapodes.jl/pull/297/" "-")))

(define plots
  (vector
   (m-picture "Co-rotating vortices on a sphere" "imgs/vort.gif" "A gif of 6 co-rotating point vortices according to the Navier-Stokes equations")
   (m-picture "Brusselator reaction on a teapot" "imgs/brusselator_teapot.gif" "A gif of the Brusselator autocatalytic reaction on the classic teapot mesh")
   (m-picture "Brusselator reaction on a square" "imgs/brusselator_square.gif" "A gif of the Brusselator autocatalytic reaction on the unit square")
   (m-picture "Brusselator reaction on a sphere" "imgs/brusselator_sphere.gif" "A gif of the Brusselator autocatalytic reaction on the unit sphere")
   (m-picture "Cahn-Hilliard equation on a square" "imgs/cahnhilliard.gif" "A gif of the Cahn-Hilliard phasefield equation")
   (m-picture "Budyko-Sellers climate model" "imgs/budyko_sellers.gif" "A gif of the Budyko-Sellers climate model")
   (m-picture "Burgers' equation" "imgs/burger_low_dif.gif" "A gif of Burger's Equation on a line")
   (m-picture "Gray-Scott reaction on a square" "imgs/gray_scott_square.gif" "A gif of the Gray-Scott reaction on the unit square")
   (m-picture "\"Halfar's dome\"" "imgs/ice_dynamics_cism.gif" "A gif of Halfar's equation on a plane")
   (m-picture "Halfar's equation on PIOMAS data" "imgs/piomas_after.png" "PIOMAS ice thickness diffused on a globe")
   (m-picture "Fluid Energetic Electron Dissipation" "imgs/kim.gif" "A gif of electron flux")
   (m-picture "\"Veronis\" lightning model" "imgs/veronis.gif" "A gif of a lightning strike")
   (m-picture "Klausmeier's vegetation model" "imgs/klausmeier.gif" "A gif of traveling vegetation waves")
   (m-picture "Gompertz growth oncology model" "imgs/gompertz.png" "Tumor proliferation")
   (m-picture "Porous media flow" "imgs/porous.gif" "A gif of flow in porous media")))

(define diagrams
  (vector
   (m-string-diagram "Streamfunction-vorticity form of the incompressible Navier-Stokes equations" "imgs/vort.svg" #:width "150px")
   (m-string-diagram "Brusselator auto-catalytic reaction" "imgs/bruss.svg")
   (m-string-diagram "Gray-Scott reaction-diffusion" "imgs/grayscott.svg")
   (m-string-diagram "Burgers' equation" "imgs/burgers.svg")
   (m-string-diagram "Budyko-Sellers climate model" "imgs/budykosellers.svg")
   (m-string-diagram "Cahn-Hilliard equation" "imgs/cahnhilliard.svg")
   (m-string-diagram "Halfar's equation" "imgs/halfar.svg")
   (m-string-diagram "Kim's Fluid Energetic Electron Dissipation (FEED)" "imgs/kim.svg")
   (m-string-diagram "Klausmeier vegetation model" "imgs/klausmeier.svg")
   (m-string-diagram "Gompertz tumor proliferation-invasion model" "imgs/oncology.svg")
   (m-string-diagram "Porous convection" "imgs/porous.svg")
   (m-string-diagram "Veronis, Inan, Pasko, Bell lightning model" "imgs/veronis.svg")))

(define scenarios
  (vector
   (m-scenario "Vorticity" 0 0)
   (m-scenario "Brusselator Teapot" 1 1)
   (m-scenario "Brusselator Square" 2 1)
   (m-scenario "Brusselator Sphere" 3 1)
   (m-scenario "Halfar Dome" 8 6)
   (m-scenario "Halfar PIOMAS" 9 6)
   (m-scenario "Gray-Scott Sphere" 7 2)
   (m-scenario "FEED" 10 7)
   (m-scenario "Veronis" 11 11)
   (m-scenario "Klausmeier" 12 8)
   (m-scenario "Budyko-Sellers" 5 4)
   (m-scenario "Cahn-Hilliard" 4 5)
   (m-scenario "Oncology" 13 9)
   (m-scenario "Porous" 14 10)
   (m-scenario "Burgers" 6 3)))

#| Time Helper Functions |#
(define months (vector "January" "February" "March" "April" "May" "June"
                       "July" "August" "September" "October" "November" "December"))
(define (pretty-date day-code)
  (format "~a ~a, ~a"
          (substring (vector-ref months (- (second day-code) 1)) 0 3)
          (first day-code)
          (third day-code)))
(define (seconds->days s) (floor (/ (/ (/ s 60) 60 ) 24)))
(define (mdy day-code) (append '(0 0 0) day-code))
(define (days-since day)
  (number->string (seconds->days
                   (- (current-seconds)
                      (apply find-seconds day)))))
(define days-since-record (days-since (mdy (record-day-code (second records)))))
(define days-since-entry (argmin string->number
                                 (map (λ (x) (days-since (mdy (record-day-code x))))
                                      records)))

#| Handle user input |#
(define (check-option lst)
  (and (not (empty? lst)) (equal? (car lst) "T")))

(define-values (show-leaderboard show-plots show-diagrams)
  (let* ([bindings (get-bindings/get)]
         [show-leaderboard-check (extract-bindings "show-leaderboard" bindings)]
         [show-plots-check (extract-bindings "show-plots" bindings)]
         [show-diagrams-check (extract-bindings "show-diagrams" bindings)])
    (values
     (check-option show-leaderboard-check)
     (check-option show-plots-check)
     (check-option show-diagrams-check))))

;; A boolean HTML attribute is (conventionally) only allowed to be set to the name of that attribute.
;; Otherwise, it should not be present.
(define (bool-attribute bool attr)
  (if bool (list (string->symbol (~a attr ":")) attr) '()))
(define (checked-attr checked?)
  (bool-attribute checked? "checked"))

;; A widget for checkboxes that hide elements according to a globabl variable.
(define (hiding-checkbox to-show)
  (define id (~a "show-" to-show))
  (define label-val (string-titlecase to-show))
  (define checked (checked-attr (eval (string->symbol id) ns)))
  (div class:"hiding-checkbox"
       (label for: id label-val)
       (apply element 'input 'type: "checkbox" 'id: id 'name: id 'value: "T" checked)))

(define view-configuration
  (form action:"./dlb.cgi" method:"GET"
        (hiding-checkbox "leaderboard") (hiding-checkbox "plots") (hiding-checkbox "diagrams")
        (input type:"submit" value:"Show")))

#| Styles |#
(define theme-base "#4A7C82")
(define theme-accent1 "orangered")
(define theme-accent2 "coral")
(define main-text-color "white")
(define regular-shadowing (~a "color: "main-text-color"; text-shadow:2px 2px 1px "theme-accent1";"))
(define styles
  (style
   (~a "
        body { font-family: -apple-system, BlinkMacSystemFont, arial; background-color:"theme-base";
               position: relative; width: 100%; padding: 0; margin: 0; }
        table, th, td { border-style: ridge}
        pre { color: white; display:block; margin-left:auto; margin-right:auto; font-size:10px;
              background-color: black; max-width: 600px; border-radius: 10%;
              border: 6px ridge "theme-accent1"; }
        p {      color: "main-text-color"; }
        a {      color: "theme-accent2"; text-shadow:1px 1px 1px "theme-accent1"; }
        strong { "regular-shadowing" }
        h1 {     "regular-shadowing" margin-top: 0em; margin-left: 0.5em; }
        h3 {     "regular-shadowing" margin-top: 1em; }
        h4 {     "regular-shadowing" margin-top: 0.75em; margin-left: 0.5em; }
        h5 {     color: "main-text-color"; }

        .picture-frame { width: 300px; display: block; margin-bottom: 1em;
                         border-radius: 10%; border: 3px ridge "theme-accent1"; }
        .physics-title { color: "main-text-color"; width: 300px; display: block; text-align: center;
                         margin-bottom: 0.5em; text-shadow:2px 2px 1px "theme-accent1"; }
        .floating-header { position: fixed; top: 0px; height: 7em; width: 100%; padding: 0; margin: 0;
                           background-color:"theme-accent2"; border-style:none none dashed none;
                           border-color: "theme-base"; }
        .main-content { margin-top: 9em; margin-left: 1em; margin-right: 1em; margin-bottom: 2em; }
        .footnote { margin-top: 5px; }
        .hiding-checkbox { float: left; margin: 1px; padding:2px; }
        .plot-and-diagram { display: flex; flex-wrap: wrap; justify-content: center; }")))
(define (a-record rec)
  (a href: (record-link rec) (record-multiphysics rec)))

#| Floating Header |#
(define (floating-header)
  (div class:"floating-header"
       (h1 "Decapodes Leader Board")
       (h4 (date->string (current-date))
           (view-configuration))))

#| Instructions |#
(define (instructions)
  (unless (or show-leaderboard show-plots show-diagrams)
    (div style:"margin-top: 5em;"
         (h5 style:"font-style: italic" "Show the leaderboard, simulation GIFs, and/ or Decapode diagrams by selecting options at the top menu."))))

#| Records Announcement |#
(define (records-announcement)
  (when show-leaderboard
    (div style:"margin-top: 5em;"
         (h5 "It has been " (strong days-since-record) " days since a new Decapodes world record.")
         (h5 "It has been " (strong days-since-entry) " days since a new Decapodes entry."))))

#| Records Table i.e. The Leader Board |#
(define (leader-board)
  (when show-leaderboard
    (div
     (table
      (tr (th "Date") (th "Initials") (th "Multiphysics") (th "Dev Time"))
      (let ([fcount 0])
        (map
         (λ (rec)
           (tr
            (td style:"text-align-last: justify; " (pretty-date (record-day-code rec)))
            (td (record-initials rec))
            (td (a-record rec))
            (td (if (non-empty-string? (record-fnote rec))
                    (begin
                      (set! fcount (add1 fcount))
                      (~a (record-dev-time rec) (make-string fcount #\*)))
                    (record-dev-time rec)))))
         records)))
     (hr))))

;; A widget for a plot with a title.
(define (plot-and-title pic)
  (div
   (i class: "physics-title" (picture-title pic))
   (img class: "picture-frame" style: (~a "width: "(picture-width pic))
        src: (picture-src pic) alt: (picture-alt pic))))

(define (scenario-showcase)
  (when (or show-plots show-diagrams)
    (div (vector->list (vector-map
                        (λ (scn)
                          (div (let
                                   ([plot (vector-ref plots (scenario-has-plot scn))]
                                    [diag (vector-ref diagrams (scenario-has-diagram scn))])
                                 (div (div class:"plot-and-diagram"
                                           (when show-plots (plot-and-title plot))
                                           (when show-diagrams (plot-and-title diag)))
                                      (hr)))))
                        scenarios)))))

#| Decapodes Overview |#
(define (example-decapode-macro)
  (pre style: "width:32em" (code "
 # Here, we declare our variables.

 (U, V)::Form0       # State variables.
 (U2V, One)::Form0   # Named intermediate variables.
 (U̇, V̇)::Form0       # Tangent variables.
 (γ, β, α)::Constant # Scalars.
 F::Parameter        # Time-varying parameter.

 # These equations relate our physical quantities.

 U2V == (U .* U) .* V

 U̇ == One + U2V - (γ * U) + (α * Δ(U)) + F
 V̇ == (β * U) - U2V + (α * Δ(U))

 # These equations specify the derivatives with
 # respect to time of our state variables.

 ∂ₜ(U) == U̇
 ∂ₜ(V) == V̇

")))

(define (example-solve)
  (pre style: "width:30em" (code "
 CahnHilliard = @decapode begin
   C::Form0
   (D, γ)::Constant
   ∂ₜ(C) == D * Δ(C.^3 - C - γ * Δ(C))
 end
 
 sim = evalsim(CahnHilliard)
 f = sim(sd, nothing);
 
 # u₀ contains initial conditions.
 prob = ODEProblem(f, u₀, (0, 200), constants)
 soln = solve(prob, Tsit5());
 
")))

(define (acronym str)
  (map (λ (x) (if (char-upper-case? x) (strong x) x)) (string->list str)))

(define (decapodes-overview)
  (div
   (h3 style: "float: left; padding-bottom:0em; margin-bottom:0em" "What is a Decapode?")
   (i class:"physics-title" style: "display: block; width: 150px; text-align: center; color: white; margin-bottom: 0.5em; margin-left: auto; margin-right:0;" align: "right" "The Diffusion Decapode")
   (img class:"picture-frame" style: "width: 150px;" align: "right" src: "imgs/diffusion.svg" alt: "A Decapode multiphysics diagram encoding diffusion")
   (p "A " (strong "Decapode") " is a diagram of a system of multiphysics equations. That's all you need to know to start if you are a physicist looking to model fluid flow, or a chemist looking to model the reaction of some chemical species. However, people familiar with graph theory can understand these as something like directed acyclic graphs (" (strong "DAGs") "), where nodes are physical quantities, and edges are operators that relate them. People familiar with category theory will suspect that " (i "diagram") " carries a connotation of " (strong "composability") " of morphisms. That is, an arrow from A to B, and an arrow from B to C, can be understood as an arrow from A to C in its own right. People even more familiar with category theory can understand these as " (a href: "https://ncatlab.org/nlab/show/copresheaf" "copresheaves") " from some category acting like a database schema. Or, as people familiar with Catlab.jl will understand them, as a certain type of " (a href:"https://algebraicjulia.github.io/Catlab.jl/v0.12/apis/categorical_algebra/#Acsets" "Acset") ".")
   (h3 "What makes constructing Decapodes fast?")
   (p "Constructing Decapodes is fast because you specify them exactly how you write your PDEs written in the Discrete Exterior Calculus.")
   (p "For example, we can write the equations for the Brusselator reaction like so:")
   (example-decapode-macro)
   (p "Constructing complex multiphysics systems from simpler, component systems is fast because we use the technique of operadic composition. That is, we can construct complex multiphysics systems by declaring variables which are shared between components:")
   (i class:"physics-title" style: "display:block; margin-left:auto; margin-right:auto; width: 150px; text-align: center; color: white; margin-bottom: 0.5em; margin-left: auto; " "A climate model composition pattern")
   (img class:"picture-frame" style: "display:block; margin-left:auto; margin-right:auto; width: 325px;" src: "imgs/bshw.svg" alt: "A composition diagram involving a Budyko-Sellers component, a melting component, a warming component, and a Halfar ice dynamics component.")
   (p "Rather than slowing us down, having formal descriptions of multiphysics diagrams enables us to develop models more quickly by providing all the information that you need to encode your multiphysics upfront.")
   (h3 "What makes Decapodes simulations fast?")
   (p "Decapodes' operators are implemented as matrix-vector multiplications or kernel operations. This is a property of the Discrete Exterior Calculus. Compounding on this, the auto-generated simulations consist of performant Julia code, and interface nicely with Julia packages like " (a href:"https://docs.sciml.ai/DiffEqDocs/stable/" "DifferentialEquations.jl") ":")
   (example-solve)
   (h3 "What makes Decapodes accurate?")
   (p "Decapodes are written in the Discrete Exterior Calculus (DEC). In the DEC, discrete operators obey the same useful laws that they obey in the continuous case. One is that the exterior derivative, d, exhibits the property that dd = 0. This is sometimes called " (a href:"https://en.wikipedia.org/wiki/Mimesis_(mathematics)" "mimesis")".")
   (h3 "What makes Decapodes iterable?")
   (p "Decapodes are written in an embedded domain-specific language (eDSL). You do not have to worry about time spent in developing a simulator for your new model because Decapodes.jl will automatically generate the simulation code for you! This allows an applied scientist to iterate through the scientific method: creating a hypothesis model and then seek to validate (or invalidate) it quickly.")
   (p "Furthermore, a Decapodes simulation generalizes over any well-constructed mesh. Once you define your physics, you can run your automatically-generated simulation on the plane, the sphere, the teapot, and so on.")
   (h3 "What is the Decapodes Leader Board?")
   (p "I created the Decapodes Leader Board (DLB) as a hobby project to keep track of models that we built. However, we soon recognized that the DLB captured the essence of a new workflow that the Decapodes project enables. We emphasize the speed in which accurate simulations for novel models can be created. Of course, modelers are interested in having good models, so we always make sure that our physics are well-formed, but as developers, we want this modeling process to be as efficient as possible. We want it to be so efficient, that one could in fact \"race\" their friends in building them!")
   (p "This \"leaderboard\" is somewhat similar to the NASA " (a href:"https://kauai.ccmc.gsfc.nasa.gov/CMEscoreboard/" "CCMC CME Scoreboard") ", where community members compete to predict CMEs accurately, using pre-built models.")
   (h3 "What does Decapodes stand for?")
   (p (acronym "Discrete Exterior Calculus Applied to Partial and Ordinary Differential EquationS"))))

#| Footer |#
(define (footer)
  (when show-leaderboard
    (div style:"margin-top: 195px;"
         (let ([fcount 0])
           (map (λ (rec)
                  (when (non-empty-string? (record-fnote rec))
                    (set! fcount (add1 fcount))
                    (p class:"footnote" (~a (make-string fcount #\*) " " (record-fnote rec)))))
                records)))))

#| Main |#
(define (front-page)
  (body
   floating-header
   (div class:"main-content"
        instructions
        records-announcement
        leader-board
        scenario-showcase
        decapodes-overview)
   footer))

#| Display Page |#
(define (render-page)
  (output-http-headers)
  (output-xml (list (doctype 'html)
                    (title "Decapodes Leaderboard")
                    (meta name: "viewport" content: "width=device-width; initial-scale=1.0")
                    styles
                    front-page)))

(render-page)

