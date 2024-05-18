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

#| Timer Helper Functions |#
(define (seconds->days s) (floor (/ (/ (/ s 60) 60 ) 24)))
(define (days-since day)
  (number->string (seconds->days
                   (- (current-seconds)
                      (apply find-seconds day)))))
(define days-since-record (days-since (list 0 0 0 21 7 2023)))
(define days-since-entry (days-since (list 0 0 0 17 5 2024)))

#| Record Data |#
(struct record (day initials multiphysics link dev-time))
(define records (list
                 (record "Mar 10, 2022" "AB" "Navier-Stokes" "https://github.com/AlgebraicJulia/DECAPODES-Benchmarks" "18 months¹")
                 (record "July 21, 2023" "GR" "Teacup Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/chemistry/brusselator_teapot.jl#L177" "15 minutes*")
                 (record "Apr 7, 2023" "LM" "Gray-Scott" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/chemistry/gray_scott.jl" "15 minutes")
                 (record "Feb 17, 2023" "GR" "Icosphere-Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/brusselator/brusselator.jl#L177" "15 minutes*")
                 (record "Sep 1, 2023" "LM & GR" "Burger's" "https://github.com/AlgebraicJulia/Decapodes.jl/pull/145" "30 minutes")
                 (record "July 13, 2023" "LM" "Nonhydrostatic Buoyant Seawater" "https://algebraicjulia.github.io/Decapodes.jl/dev/nhs/" "4 hours")
                 (record "July 12, 2023" "LM" "Halfar" "https://algebraicjulia.github.io/Decapodes.jl/dev/cism/" "2 hours")
                 (record "July 11, 2023" "LM" "Budyko-Sellers" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/climate/budyko_sellers.jl" "2 hours")
                 (record "Feb 16, 2023" "LM & GR" "Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/brusselator/brusselator.jl" "2 hours")
                 (record "May 17, 2024" "LM" "Navier-Stokes, Vorticity" "https://algebraicjulia.github.io/Decapodes.jl/dev/navier_stokes/ns/" "2 hours")
                 (record "Feb  7, 2023" "LM & JC & JG" "Multispecies Navier-Stokes" "https://github.com/AlgebraicJulia/Decapodes.jl/issues/70#issuecomment-1421598346" "5 hours**")))

#| Set up the page |#
(define ox output-xml)
(define (output-setup)
  (output-http-headers)
  (ox (doctype 'html))
  (ox (meta name: "viewport" content: "width=device-width; initial-scale=1.0")))

#| Styles |#
(define theme-base "#5B9AA0")
(define theme-accent "orangered")
(define theme-accent2 "coral")
(define theme-accent3 "white")
(define (styles)
  (list 
   (style (~a "body { font-family: arial; background-color:"theme-base"; position: relative; width: 100%; padding: 0; margin: 0; }
            th, td { border-style: ridge}
            a { color:" theme-accent2 "; text-shadow:1px 1px 1px "theme-accent";}
            strong { color:"theme-accent3"; text-shadow:2px 2px 1px "theme-accent";}
            p { color:"theme-accent3";}
            h1 { margin-top: 1em; margin-left: 0.5em; color: "theme-accent3"; text-shadow:2px 2px 1px "theme-accent"; }
            h3 { margin-top: 1em; color: "theme-accent3"; text-shadow:2px 2px 1px "theme-accent";}
            h4 { margin-top: 0.75em; position: fixed; margin-right: 0.5em; float: right; top: 0; right: 0; color: "theme-accent3"; text-shadow:2px 2px 1px "theme-accent"; }
            h5 { color: "theme-accent3"; }
            table { border-style: ridge; }"))
   (style (~a ".picture-frame { width: 300px; display: block; margin-bottom: 1em; border-radius: 10% 10% 10% 10%; border: 3px ridge "theme-accent"; }"))
   (style (~a ".physics-title { width: 300px; display: block; text-align: center; color: "theme-accent3"; margin-bottom: 0.5em; text-shadow:2px 2px 1px "theme-accent"; }"))
   (style (~a ".floating-header { position: fixed; top: 0px; height: 5em; width: 100%; padding: 0; margin: 0; background-color:coral; border-style:none none dashed none; border-color: #5B9AA0; }"))
   (style (~a ".main-content { margin-left: 1em; margin-right: 0.5em; }"))
   (style (~a ".footnote { margin-top: 5px; }"))
   (style (~a ".gallery { display: grid; grid-template-columns: repeat(4, 1fr); grid-template-rows: masonry; }"))))

#| Floating Header |#
(define floating-header
  (div class:"floating-header"
       (h1 "Decapodes Leader Board")
       (h4 (date->string (current-date)))))

#| Records Announcement |#
(define records-announcement
  (div style:"margin-top: 5em;"
       (h5 "It has been " (strong days-since-record) " days since a new Decapodes world record.")
       (h5 "It has been " (strong days-since-entry) " days since a new Decapodes entry.")))

#| Records Table i.e. The Leader Board |#
(define leader-board
  (table
   (tr
    (th "Date") (th "Initials") (th "Multiphysics") (th "Dev Time"))
   (map (λ (rec)
          (tr (td (record-day rec)) (td (record-initials rec)) (td (a href: (record-link rec) (record-multiphysics rec))) (td (record-dev-time rec)))) records)))

#| Gallery |#
(struct picture (title src alt))
(define pictures (list
                  (picture "Multispecies Navier-Stokes" "imgs/multispecies.gif" "A gif of a multispecies Navier-Stokes simulation")
                  (picture "Brusselator Reaction" "imgs/brusselator_square.gif" "A gif of the Brusselator autocatalytic reaction on the unit square")
                  (picture "Icosphere Brusselator Reaction" "imgs/brusselator_sphere.gif" "A gif of the Brusselator autocatalytic reaction on the unit sphere")
                  (picture "Teapot Brusselator Reaction" "imgs/brusselator_teapot.gif" "A gif of the Brusselator autocatalytic reaction on the classic teapot mesh")
                  (picture "Gray-Scott Reaction" "imgs/gray_scott_square.gif" "A gif of the Gray-Scott reaction on the unit square")
                  (picture "Budyko-Sellers Climate Model" "imgs/budyko_sellers.gif" "A gif of the Budyko-Sellers climate model")
                  (picture "Burger's Equation" "imgs/burger_low_dif.gif" "A gif of Burger's Equation on a line")))
(define gallery
  (div class:"gallery"
       (map (λ (ge)
              (div
               (i class: "physics-title" (picture-title ge))
               (img class: "picture-frame" src: (picture-src ge) alt: (picture-alt ge)))) pictures)))

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
   (p "A " (strong "Decapode") " is a diagram of a system of multiphysics equations. That's all you need to know to start if you are a physicist looking to model fluid flow, or a chemist looking to model the reaction of some chemical species. However, people familiar with graph theory can understand these as something like directed acyclic graphs (" (strong "DAGs") "), where nodes are physical quantities, and edges are operators that relate them. People familiar with category theory will suspect that " (i "diagram") " carries a connotation with it of " (strong "composability") " of morphisms. That is, an arrow from A to B, and an arrow from B to C, can be understood as an arrow from A to C in its own right. People even more familiar with category can understand these as " (a href: "https://ncatlab.org/nlab/show/copresheaf" "copresheaves") " from some category acting like a database schema. Or, as people familiar with Catlab.jl will understand them, as a certain type of " (a href:"https://algebraicjulia.github.io/Catlab.jl/v0.12/apis/categorical_algebra/#Acsets" "Acset") ". But that's just what a Decapode is. What else is there to Decapodes?")
   (h3 "What makes constructing Decapodes fast?")
   (p "Constructing Decapodes is fast because you specify them exactly how you write your PDEs written in the Discrete Exterior Calculus.")
   (p "For example, we can write the equations for the Brusselator reaction like so:")
   (example-decapode-macro)
   (p "Constructing complex multiphysics systems from simpler, component systems is fast because we use the technique of operadic composition. That is, we can describe complex multiphysics systems from which variables are shared between component systems.")
   (p "Rather than slowing us down, having formal descriptions of multiphysics diagrams enables us to develop models more quickly by providing all the information that you need to encode your multiphysics upfront.")
   (h3 "What makes Decapodes simulations fast?")
   (p "Decapodes simulations are fast because their operators are implemented as matrix-matrix and matrix-vector multiplications. This is a property of the Discrete Exterior Calculus. Compounding on this, the auto-generated simulations consist of performant Julia code, and interface nicely with Julia packages like OrdinaryDiffEq.jl and MultiScaleArrays.jl.")
   (h3 "What makes Decapodes accurate?")
   (p "Decapodes simulations are accurate because they use the Discrete Exterior Calculus (DEC). The DEC has the amazing property that the operators obey the same useful laws that they obey in the continuous case. One is that the exterior derivative, d, exhibits the property that dd = 0.")
   (h3 "What makes Decapodes iterable?")
   (p "Decapodes are iterable because new models can be written quickly. You do not have to worry about time spent in developing a simulator for your new model because Decapodes.jl will automatically generate the simulator for you! They allow a scientist to use the scientific method of creating a hypothesis model and then seek to validate (or rather disprove) it quickly.")
   (p "Furthermore, a Decapodes simulation generalizes over any well-constructed mesh. Once you define your physics, you can run your automatically-generated simulation on the plane, the sphere, and so on.")
   (h3 "What is the Decapodes Leader Board?")
   (p "I (Luke Morris) created the Decapodes Leader Board (DLB) initially as a hobby project to keep track of the models that we built for a friend over coffee. However, we soon recognized that the DLB captured the essence of a new workflow that the Decapodes project enables. We emphasize the speed in which accurate simulations for novel models can be created. Of course, modelers are interested in having good models, so we always make sure that our physics are well-formed, but as developers, we want this modeling process to be as efficient as possible. We want it to be so efficient, that one could in fact \"race\" their friends in building them!")
   (h3 "What does Decapodes stand for?")
   (p (acronym "Discrete Exterior Calculus Applied to Partial and Ordinary Differential Equations"))
   #| -Embedded in a programming language
                   -Fast (Because of the DEC.)
                   -Accurate (Because of the DEC.)
                   -Composable (Because of ACT formalization)
                   -Iterable|#
   (h5 "Site under construction")))

#| Footer |#
(define footer
  (div style:"margin-top: 195px;"
       (p class:"footnote" "¹: Honorary permanent number one")
       (p class:"footnote" "*: Extending a simulation from the unit square to the unit sphere")
       (p class:"footnote" "**: Starting from pre-formulated Navier-Stokes Decapode")))

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
        #| Gallery |#
        (hr)
        (gallery)
        #| Decapodes overview |#
        (hr)
        (decapodes-overview))
   #| Footer |#
   (footer)))

#| Display Page |#
(output-setup)
(ox styles)
(ox front-page)
