#!/cise/homes/luke.morris/local/bin/racket

#lang racket/base

#|
Author: Luke Lawlor Morris
This CGI is meant to keep track of multiphysics simulations in a leader-board format.
|#

(require net/cgi)
(require scribble/html) 
(require syntax/to-string)
(require racket/date)
(require racket/format)
(require racket/vector)
(require racket/treelist)

(define-namespace-anchor ns-a)
(define ns (namespace-anchor->namespace ns-a))

#| Record Data |#
(struct record (day-code initials multiphysics link dev-time))
(define records
  (list
   (record '(10 3 2022) "AB" "Navier-Stokes" "https://github.com/AlgebraicJulia/DECAPODES-Benchmarks" "18 months¹")
   (record '(24 4 2024) "GR" "Cahn-Hilliard" "https://algebraicjulia.github.io/Decapodes.jl/dev/ch/cahn-hilliard/" "10 minutes")
   (record '(21 7 2023) "GR" "Teacup Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/chemistry/brusselator_teapot.jl#L177" "15 minutes*")
   (record '(7  4 2023) "LM" "Gray-Scott" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/chemistry/gray_scott.jl" "15 minutes")
   (record '(17 2 2023) "GR" "Icosphere-Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/brusselator/brusselator.jl#L177" "15 minutes*")
   (record '(1  9 2023) "LM & GR" "Burgers'" "https://github.com/AlgebraicJulia/Decapodes.jl/pull/145" "30 minutes")
   (record '(12 7 2023) "LM" "Halfar" "https://algebraicjulia.github.io/Decapodes.jl/dev/cism/" "2 hours")
   (record '(11 7 2023) "LM" "Budyko-Sellers" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/climate/budyko_sellers.jl" "2 hours")
   (record '(16 2 2023) "LM & GR" "Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/brusselator/brusselator.jl" "2 hours")
   (record '(17 5 2024) "LM" "Navier-Stokes, Vorticity" "https://algebraicjulia.github.io/Decapodes.jl/dev/navier_stokes/ns/" "2 hours")
   (record '(13 7 2023) "LM" "Nonhydrostatic Buoyant Seawater" "https://algebraicjulia.github.io/Decapodes.jl/dev/nhs/" "4 hours")
   (record '(7  2 2023) "LM & JC & JG" "Multispecies Navier-Stokes" "https://github.com/AlgebraicJulia/Decapodes.jl/issues/70#issuecomment-1421598346" "5 hours**")
   (record '(9  5 2024) "LM" "Vorticity Navier-Stokes" "https://algebraicjulia.github.io/Decapodes.jl/dev/navier_stokes/ns/" "-")))

#| Time Helper Functions |#
(define months (vector "January" "February" "March" "April" "May" "June" "July" "August" "September" "October" "November" "December"))
(define (pretty-date day-code)
  (format "~a ~a, ~a"
          (substring (vector-ref months (- (second day-code) 1)) 0 3)
          (first day-code)
          (third day-code)))
(define (seconds->days s) (floor (/ (/ (/ s 60) 60 ) 24)))
(define (days-since day)
  (number->string (seconds->days
                   (- (current-seconds)
                      (apply find-seconds day)))))
(define days-since-record (days-since (append '(0 0 0) (record-day-code (second records)))))
(define days-since-entry (argmin string->number (map (λ (x) (days-since (append '(0 0 0) (record-day-code x)))) records)))

#| Set up the page |#
(define ox output-xml)
(define (output-setup)
  (output-http-headers)
  (ox (doctype 'html))
  (ox (meta name: "viewport" content: "width=device-width; initial-scale=1.0")))

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
;; otherwise, it should not be present.
(define (bool-attr bool attr)
  (cond
    [bool (list (string->symbol (string-append attr ":")) attr)]
    [else '()]))
(define (checked-attr to-check)
  (bool-attr to-check "checked"))

(define (hiding-checkbox to-show)
  (define id (string-append "show-" to-show))
  (define label-val (string-titlecase to-show))
  (define active-var (string->symbol id))
  (div class:"hiding-checkbox"
       (element 'label 'for: id label-val)
       (apply element 'input 'type: "checkbox" 'id: id 'name: id 'value: "T"
              (checked-attr (eval active-var ns)))))

(define view-configuration
  (form action:"./dlb.cgi" method:"GET"
        (hiding-checkbox "leaderboard") (hiding-checkbox "plots") (hiding-checkbox "diagrams")
        (input type:"submit" value:"Show")))

#| Styles |#
(define theme-base "#5B9AA0")
(define theme-accent "orangered")
(define theme-accent2 "coral")
(define theme-accent3 "white")
(define (styles)
  (list 
   (style (~a "
            body { font-family: arial; background-color:"theme-base"; position: relative; width: 100%; padding: 0; margin: 0; }
            table, th, td { border-style: ridge}
            a {      color: "theme-accent2"; text-shadow:1px 1px 1px "theme-accent";}
            p {      color: "theme-accent3";}
            strong { color: "theme-accent3"; text-shadow:2px 2px 1px "theme-accent";}
            h1 {     color: "theme-accent3"; text-shadow:2px 2px 1px "theme-accent"; margin-top: 0em; margin-left: 0.5em; }
            h3 {     color: "theme-accent3"; text-shadow:2px 2px 1px "theme-accent"; margin-top: 1em; }
            h4 {     color: "theme-accent3"; text-shadow:2px 2px 1px "theme-accent"; margin-top: 0.75em; margin-left: 0.5em; }
            h5 {     color: "theme-accent3"; }"))
   (style (~a ".picture-frame { width: 300px; display: block; margin-bottom: 1em; border-radius: 10% 10% 10% 10%; border: 3px ridge "theme-accent"; }"))
   (style (~a ".physics-title { width: 300px; display: block; text-align: center; color: "theme-accent3"; margin-bottom: 0.5em; text-shadow:2px 2px 1px "theme-accent"; }"))
   (style (~a ".floating-header { position: fixed; top: 0px; height: 7em; width: 100%; padding: 0; margin: 0; background-color:coral; border-style:none none dashed none; border-color: #5B9AA0; }"))
   (style (~a ".main-content { margin-top: 9em; margin-left: 1em; margin-right: 0.5em; }"))
   (style (~a ".footnote { margin-top: 5px; }"))
   (style (~a ".hiding-checkbox { float: left; margin: 1px; padding:2px; }"))
   (style (~a ".plot-and-diagram { display: flex; flex-wrap: wrap; }"))))

#| Floating Header |#
(define floating-header
  (div class:"floating-header"
       (h1 "Decapodes Leader Board")
       (h4 (date->string (current-date))
           (view-configuration))))

#| Records Announcement |#
(define records-announcement
  (cond
    [show-leaderboard
     (div style:"margin-top: 5em;"
          (h5 "It has been " (strong days-since-record) " days since a new Decapodes world record.")
          (h5 "It has been " (strong days-since-entry) " days since a new Decapodes entry."))]
    [else (div)]))

#| Records Table i.e. The Leader Board |#
(define leader-board
  (cond
    [show-leaderboard
     (div
      (table
       (tr (th "Date") (th "Initials") (th "Multiphysics") (th "Dev Time"))
       (map (λ (rec)
              (tr (td style:"text-align-last: justify; " (pretty-date (record-day-code rec))) (td (record-initials rec)) (td (a href: (record-link rec) (record-multiphysics rec))) (td (record-dev-time rec))))
            records))
      (hr))]
    [else (div)]))

#| Database of Plots and Diagrams |#
(struct picture (title src alt width))
(define (m-picture title src alt #:width [width "300px"])
  (picture title src alt width))

(define plots
  (treelist
   (m-picture "Co-rotating vortices on a sphere" "imgs/vort.gif" "A gif of 6 co-rotating point vortices according to the Navier-Stokes equations")
   (m-picture "Brusselator reaction on a teapot" "imgs/brusselator_teapot.gif" "A gif of the Brusselator autocatalytic reaction on the classic teapot mesh")
   (m-picture "Brusselator reaction on a square" "imgs/brusselator_square.gif" "A gif of the Brusselator autocatalytic reaction on the unit square")
   (m-picture "Brusselator reaction on a sphere" "imgs/brusselator_sphere.gif" "A gif of the Brusselator autocatalytic reaction on the unit sphere")
   (m-picture "Cahn-Hilliard equation on a square" "imgs/cahnhilliard.gif" "A gif of the Cahn-Hilliard phasefield equation")
   (m-picture "Budyko-Sellers climate model" "imgs/budyko_sellers.gif" "A gif of the Budyko-Sellers climate model")
   (m-picture "Burgers' equation" "imgs/burger_low_dif.gif" "A gif of Burger's Equation on a line")
   (m-picture "Gray-Scott reaction on a square" "imgs/gray_scott_square.gif" "A gif of the Gray-Scott reaction on the unit square")))

(define diagrams
  (treelist
   (m-picture "Streamfunction-vorticity form of the incompressible Navier-Stokes equations" "imgs/vort.svg" "A string diagram" #:width "150px")
   (m-picture "Brusselator auto-catalytic reaction" "imgs/bruss.svg" "A string diagram")
   (m-picture "Gray-Scott reaction-diffusion" "imgs/grayscott.svg" "A string diagram")
   (m-picture "Burgers' equation" "imgs/burgers.svg" "A string diagram")
   (m-picture "Budyko-Sellers climate model" "imgs/budykosellers.svg" "A string diagram")
   (m-picture "Cahn-Hilliard equation" "imgs/cahnhilliard.svg" "A string diagram")))

(struct scenario (name plot-key diagram-key))

(define scenarios
  (treelist
   (scenario "Vorticity" 0 0)
   (scenario "Brusselator Teapot" 1 1)
   (scenario "Brusselator Square" 2 1)
   (scenario "Brusselator Sphere" 3 1)
   (scenario "Gray-Scott Sphere" 7 2)
   (scenario "Budyko-Sellers" 5 4)
   (scenario "Cahn-Hilliard" 4 5)
   (scenario "Burgers" 6 3)))

;; A widget for a plot with a title.
(define (plot-and-title pic)
  (div
   (i class: "physics-title" (picture-title pic))
   (img class: "picture-frame" style: (~a "width: "(picture-width pic)) src: (picture-src pic) alt: (picture-alt pic))))

(define scenario-showcase
  (cond
    [(or show-plots show-diagrams)
     (div
      (treelist->list
       (treelist-map
        scenarios
        (λ (scn)
          (div
           (let*
               ([plot (treelist-ref plots (scenario-plot-key scn))]
                [diag (treelist-ref diagrams (scenario-diagram-key scn))])
             (div
              (div class:"plot-and-diagram"
                   (cond [show-plots (plot-and-title plot)])
                   (cond [show-diagrams (plot-and-title diag)]))
              (hr))))))))]
    [else (div)]))

#| Decapodes Overview |#
(define example-decapode-macro
  (pre style:"color: white; background-color: black; max-width: 800px;" (code "
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

(define (acronym str)
  (map (λ (x) (if (char-upper-case? x) (strong x) x)) (string->list str)))

(define decapodes-overview
  (div
   (h3 style: "float: left; padding-bottom:0em; margin-bottom:0em" "What is a Decapode?")
   (i style: "display: block; width: 150px; text-align: center; color: white; margin-bottom: 0.5em; text-shadow:2px 2px 1px orangered; margin-left: auto; margin-right:0;" align: "right" "The Diffusion Decapode")
   (img class:"picture-frame" style: "width: 150px;" align: "right" src: "imgs/diffusion.svg" alt: "A Decapode multiphysics diagram encoding diffusion")
   (p "A " (strong "Decapode") " is a diagram of a system of multiphysics equations. That's all you need to know to start if you are a physicist looking to model fluid flow, or a chemist looking to model the reaction of some chemical species. However, people familiar with graph theory can understand these as something like directed acyclic graphs (" (strong "DAGs") "), where nodes are physical quantities, and edges are operators that relate them. People familiar with category theory will suspect that " (i "diagram") " carries a connotation of " (strong "composability") " of morphisms. That is, an arrow from A to B, and an arrow from B to C, can be understood as an arrow from A to C in its own right. People even more familiar with category theory can understand these as " (a href: "https://ncatlab.org/nlab/show/copresheaf" "copresheaves") " from some category acting like a database schema. Or, as people familiar with Catlab.jl will understand them, as a certain type of " (a href:"https://algebraicjulia.github.io/Catlab.jl/v0.12/apis/categorical_algebra/#Acsets" "Acset") ".")
   (h3 "What makes constructing Decapodes fast?")
   (p "Constructing Decapodes is fast because you specify them exactly how you write your PDEs written in the Discrete Exterior Calculus.")
   (p "For example, we can write the equations for the Brusselator reaction like so:")
   (example-decapode-macro)
   (p "Constructing complex multiphysics systems from simpler, component systems is fast because we use the technique of operadic composition. That is, we can describe complex multiphysics systems from which variables are shared between component systems.")
   (p "Rather than slowing us down, having formal descriptions of multiphysics diagrams enables us to develop models more quickly by providing all the information that you need to encode your multiphysics upfront.")
   (h3 "What makes Decapodes simulations fast?")
   (p "Decapodes simulations are fast because their operators are implemented as matrix-vector multiplications or kernel operations. This is a property of the Discrete Exterior Calculus. Compounding on this, the auto-generated simulations consist of performant Julia code, and interface nicely with Julia packages like " (a href:"https://docs.sciml.ai/DiffEqDocs/stable/" "DifferentialEquations.jl") ".")
   (h3 "What makes Decapodes accurate?")
   (p "Decapodes simulations are accurate because they use the Discrete Exterior Calculus (DEC). In the DEC, discrete operators obey the same useful laws that they obey in the continuous case. One is that the exterior derivative, d, exhibits the property that dd = 0. This is sometimes called " (a href:"https://en.wikipedia.org/wiki/Mimesis_(mathematics)" "mimesis")".")
   (h3 "What makes Decapodes iterable?")
   (p "Decapodes are iterable because new models can be written quickly. You do not have to worry about time spent in developing a simulator for your new model because Decapodes.jl will automatically generate the simulation code for you! This allows an applied scientist to iterate through the scientific method: creating a hypothesis model and then seek to validate (or invalidate) it quickly.")
   (p "Furthermore, a Decapodes simulation generalizes over any well-constructed mesh. Once you define your physics, you can run your automatically-generated simulation on the plane, the sphere, the teapot, and so on.")
   (h3 "What is the Decapodes Leader Board?")
   (p "I created the Decapodes Leader Board (DLB) as a hobby project to keep track of models that we built. However, we soon recognized that the DLB captured the essence of a new workflow that the Decapodes project enables. We emphasize the speed in which accurate simulations for novel models can be created. Of course, modelers are interested in having good models, so we always make sure that our physics are well-formed, but as developers, we want this modeling process to be as efficient as possible. We want it to be so efficient, that one could in fact \"race\" their friends in building them!")
   (p "This \"leaderboard\" is somewhat similar to the NASA " (a href:"https://kauai.ccmc.gsfc.nasa.gov/CMEscoreboard/" "CCMC CME Scoreboard") ", where community members compete to predict CMEs accurately, using pre-built models.")
   (h3 "What does Decapodes stand for?")
   (p (acronym "Discrete Exterior Calculus Applied to Partial and Ordinary Differential EquationS"))))

#| Footer |#
(define footer
  (cond
    [show-leaderboard
     (div style:"margin-top: 195px;"
          (p class:"footnote" "¹: Honorary permanent number one")
          (p class:"footnote" "*: Extending a simulation from the unit square to the unit sphere")
          (p class:"footnote" "**: Starting from pre-formulated Navier-Stokes Decapode"))]
    [else (div)]))

#| Main |#
(define front-page
  (body
   #| Header |#
   (floating-header)
   #| Main Content |#
   (div class:"main-content"
        #| Days-since-new-record |#
        (records-announcement)
        #| Leader board |#
        (leader-board)
        #| Scenario showcase |#
        (scenario-showcase)
        #| Decapodes overview |#
        (decapodes-overview))
   #| Footer |#
   (footer)))

#| Display Page |#
(define (render-page)
  (output-setup)
  (ox styles)
  (ox front-page))

(render-page)
