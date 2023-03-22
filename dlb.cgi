#!/cise/homes/luke.morris/local/bin/racket

#lang racket/base

#|
This CGI is meant to keep track of multiphysics simulations in a leader-board format.
|#

(require net/cgi)
(require scribble/html) 
(require syntax/to-string)
(require racket/date)

(define (seconds->days s) (floor (/ (/ (/ s 60) 60 ) 24)))

(define days-since-record (number->string (seconds->days
    (- (current-seconds)
    (find-seconds 0 0 0 17 2 2023)))))

(struct record (day initials multiphysics link dev-time))
(define records (list
    (record "Mar 10, 2022" "AB" "Navier-Stokes" "https://github.com/AlgebraicJulia/Decapodes.jl" "18 months¹")
    (record "Feb 17, 2023" "GR" "Icosphere-Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/brusselator/brusselator.jl#L177" "15 minutes*")
    (record "Feb 16, 2023" "LM & GR" "Brusselator" "https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/brusselator/brusselator.jl" "2 hours")
    (record "Feb 14, 2023" "GR & LM" "Mohamed Flow" "https://arxiv.org/abs/1508.01166" "2 hours")
    (record "Feb  7, 2023" "LM & JC & JG" "Multispecies Navier-Stokes" "https://github.com/AlgebraicJulia/Decapodes.jl/issues/70#issuecomment-1421598346" "5 hours**")))

(struct picture-frame (multiphysics img-link width alt-text))
(define picture-frames (list
    (picture-frame "Multispecies Navier-Stokes" "imgs/multispecies.gif" "width: 300px;" "A gif of a multispecies Navier-Stokes simulation")
    (picture-frame "Brusselator Reaction" "imgs/brusselator_square.gif" "width: 300px;" "A gif of the Brusselator autocatalytic reaction on the unit square")
    (picture-frame "Icosphere Brusselator Reaction" "imgs/brusselator_sphere.gif" "width: 300px;" "A gif of the Brusselator autocatalytic reaction on the unit sphere")))

(define ox output-xml)
(output-http-headers)
(ox (doctype 'html))

(ox (meta name: "viewport" content: "width=device-width; initial-scale=1.0"))

(ox (style "th, td { border-style: ridge}
            a { color:#FF7F50; text-shadow:1px 1px 1px orangered;}
            strong { color:white; text-shadow:2px 2px 1px orangered;}
            h3 { margin-top: 1em; color: white; text-shadow:2px 2px 1px orangered;}
            p { color:white;} "))

(ox (body style:"font-family: arial; background-color:#5B9AA0; position: relative; width: 100%; padding: 0; margin: 0;"
        #| Header Div |#
        (div style:"position: fixed; top: 0px; height: 5em; width: 100%; padding: 0; margin: 0; background-color:coral; border-style:none none dashed none; border-color: #5B9AA0"
            (h1 style:"margin-top: 1em; margin-left: 0.5em; color: white; text-shadow:2px 2px 1px orangered;" "Decapodes Leader Board")
            (h4 style:"position: fixed; margin-right: 0.5em; ; margin-top: 0.75em; float: right; top: 0; right: 0; color: white; text-shadow:2px 2px 1px orangered;" (date->string (current-date))))
        #| Main Content Div |#
        (div style:"margin-left: 1em; margin-right: 0.5em;"
            #| Days-since-new-record |#
            (h5 style:"margin-top: 8em; color: white;" "It has been " (strong days-since-record) " days since a new Decapodes world record.")
            #| Records table i.e. "leader-board" |#
            (table style:"border-style: ridge;"
                (tr
                    (th "Date") (th "Initials") (th "Multiphysics") (th "Dev Time"))
                (map (lambda (rec)
                    (tr (td (record-day rec)) (td (record-initials rec)) (td (a href: (record-link rec) (record-multiphysics rec))) (td (record-dev-time rec)))) records))
            (hr)
            #| Images |#
            (div
                (i style: "display: block; width: 300px; text-align: center; color: white; margin-bottom: 0.5em; text-shadow:2px 2px 1px orangered;" "Multispecies Navier-Stokes")
                (img style: "width: 300px; display: block; margin-bottom: 1em; border-radius: 10% 10% 10% 10%; border: 3px ridge orangered;" src: "imgs/multispecies.gif" alt: "A gif of a multispecies Navier-Stokes simulation")
                (i style: "display: block; width: 300px; text-align: center; color: white; margin-bottom: 0.5em; text-shadow:2px 2px 1px orangered;" "Brusselator Reaction")
                (img style: "width: 300px; display: block; margin-bottom: 1em; border-radius: 10% 10% 10% 10%; border: 3px ridge orangered;" align: "left" src: "imgs/brusselator_square.gif" alt: "A gif of the Brusselator autocatalytic reaction on the unit square")
                (img style: "width: 300px; display: block; margin-bottom: 1em; border-radius: 10% 10% 10% 10%; border: 3px ridge orangered;" src: "imgs/brusselator.svg" alt: "A Decapode multiphysics diagram of the Brusselator reaction")
                (i style: "display: block; width: 300px; text-align: center; color: white; margin-bottom: 0.5em; text-shadow:2px 2px 1px orangered;" "Icosphere Brusselator Reaction")
                (img style: "width: 300px; display: block; border-radius: 10% 10% 10% 10%; border: 3px ridge orangered;" src: "imgs/brusselator_sphere.gif" alt: "A gif of the Brusselator autocatalytic reaction on the unit sphere"))
            #| Decapodes overview |#
            (hr)
            (div
                (h3 style: "float: left; padding-bottom:0em; margin-bottom:0em" "What is a Decapode?")
                (i style: "display: block; width: 150px; text-align: center; color: white; margin-bottom: 0.5em; text-shadow:2px 2px 1px orangered; margin-left: auto; margin-right:0;" align: "right" "The Diffusion Decapode")
                (img style: "width: 150px; display: block; margin-bottom: 1em; border-radius: 10% 10% 10% 10%; border: 3px ridge orangered;" align: "right" src: "imgs/diffusion.svg" alt: "A Decapode multiphysics diagram encoding diffusion")
                (p "A " (strong "Decapode") " is a diagram of a system of multiphysics equations. That's all you need to know to start if you are a physicist looking to model fluid flow, or a chemist looking to model the reaction of some chemical species. However, people familiar with graph theory can understand these as something like directed acyclic graphs (" (strong "DAGs") "), where nodes are physical quantities, and edges are operators that relate them. People familiar with category theory will suspect that " (i "diagram") " carries a connotation with it of " (strong "composability") " of morphisms. That is, an arrow from A to B, and an arrow from B to C, can be understood as an arrow from A to C in its own right. People even more familiar with category can understand these as " (a href: "https://ncatlab.org/nlab/show/copresheaf" "copresheaves") " from some category acting like a database schema. Or, as people familiar with Catlab.jl will understand them, as a certain type of " (a href:"https://algebraicjulia.github.io/Catlab.jl/v0.12/apis/categorical_algebra/#Acsets" "Acset") ". But that's just what a Decapode is. What else is there to Decapodes?")
                (h3 "What makes constructing Decapodes fast?")
                (p "Constructing Decapodes is fast because you specify them exactly how you write your PDEs written in the Discrete Exterior Calculus.")
		(p "For example, we can write the equations for the Brusselator reaction like so:")
		(pre style: "color: white; background-color: black; max-width: 800px;" (code
"
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

"))
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
                (p (strong "D")"iscrete "(strong "E")"xterior "(strong "C")"alculus "(strong "A")"pplied to "(strong "P")"artial and "(strong "O")"rdinary "(strong "D")"ifferential "(strong "E")"quations")
                #| -Embedded in a programming language
                   -Fast (Because of the DEC.)
                   -Accurate (Because of the DEC.)
                   -Composable (Because of ACT formalization)
                   -Iterable|#
                (h5 "Site under construction")))
        #| Footer |#
        (p style:"margin-top: 200px;" "¹: Honorary permanent number one")
        (p style:"margin-top: 5px;" "*: Extending a simulation from the unit square to the unit sphere")
        (p style:"margin-top: 5px;" "**: Starting from pre-formulated Navier-Stokes Decapode")))

