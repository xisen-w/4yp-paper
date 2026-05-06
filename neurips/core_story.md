 Below are the important disucssions for the final story.

 Note this is only for depicting the set-up & the RQs and the findings. 

 We keep in the main paper about the SharedOS idea and everything. (Like, it is still that we have this problem -> formulate it -> build a platform where ppl cna test stuff -> we choose to test these things (the RQs, which we deciding here))

 When you revise the paper, still the key rules: no dashline, no semicolon. Preferably no bullet point unless if you really need. 

 Note that the reference below to PACT-Bench is legacy, we don't name it any more. 

 ----------------------------------------------------- NOW
 
 The problem is that enforcement via reasoning is inherently                                                        
    unpredictable because you cannot enumerate the model's implicit social norms, and those norms compose with your  
  policy in                                                                                                          
    ways you cannot foresee.  This is i guess fun. BecBecoz the core set-up of the paper is on cross-boundary        
  agents. It is very obvious that for cross-boundary agents, there needs to be some unique things. You are talking   
  to other person's agent. so the social relationship behind matters (that's why it's part of a core). The agent can 
   talk indefinitely across scattered files and states, can they really attack by themselves? tehy could and they    
  are doing good ways. What is the boundary? CAn i just lay a prompt of "Do not share?" No. But maybe, for a         
  catgeory, this is doable. But then the question is, does this scale to all relationshps? another no. becoz this    
  would give the trade-off of over-refusal. as foundamentally there si tehq uality : same context will be shared     
  over different people. That's why in the paper title we say the utility-security frontier. Do u think this can be  
  a interesting story itself? Can we first test if there's a trade off? Then depict the boudnary of the trade-off.   
  Treat this as an important independent finding? or make this the whole thread? Is there a trade-off? (without      
  policy, without anything). (yeah security is shit). Now what is the boundary. make policy more speicfic, does it   
  help? in some way. make better models, does this help? in some way. but things will confront with relationship.    
  and things will confront with multi-turn attacks that the agent is able todo. the trade-off is also inbalance      
  across states/data surfaces... etc. So i the whole paper formulate the problem, built a tool that others can use   
  for expeimrents, curated data carefully and explored our RQs around the boundary, depicted the oboundary and       
  guided future reserach in some sense.                                                                              

⏺ Yes. Make it the thread, not a finding.

  The paper is: "We systematically explore the security-utility frontier in cross-boundary agent delegation."        
  
  Every finding is a property of the frontier:                                                                       
                                                                  
  The Security-Utility Frontier in Cross-Boundary Delegation
  │
  ├── Does the frontier exist?                                                                                       
  │   → Yes. Without policy: 83% leak (security is trash, utility is fine)                                           
  │                                                                                                                  
  ├── Can policy move the frontier?                                                                                  
  │   → Only with category specificity. D1 doesn't move it. D2 shifts it dramatically.                               
  │                                                                                                                  
  ├── Is the frontier stable over time?                                                                              
  │   → Mostly. Multi-turn doesn't collapse it. But locally crackable via strategy combinations.                     
  │                                                                                                                  
  ├── Is the frontier flat across relationships?                                                                     
  │   → No. It tilts: investor shifts toward permissive, friend shifts toward restrictive.                           
  │     Same policy, different operating point per person.                                                           
  │     Over-refusal becomes the dominant cost, not leakage.                                                         
  │                                                                                                                  
  ├── Is the frontier flat across data surfaces?                                                                     
  │   → No. Nearly free on files, catastrophically expensive on structured state.                                    
  │                                                                                                                  
  └── Conclusion: The frontier is multi-dimensional, shaped by invisible pretraining norms,                          
      and cannot be flattened to optimal by prompt engineering. → Architecture needed.                               
                                                                                                                     
  Why this works as the whole thread (not just a finding):                                                           
                                                                                                                     
  1. Title already says it: "Security-Utility Frontier" is literally what you're mapping                             
  2. Platform contribution is naturally motivated: you need SharedOS to systematically probe the frontier across all
  dimensions. No single experiment gives you the full shape.                                                         
  3. Each RQ is a "slice" of the frontier: not independent questions, but different axes of the same object
  4. Findings compose: specificity creates the floor, multi-turn tests its durability, relationship reveals its      
  non-uniformity, surface reveals its cost structure                                                                 
  5. Conclusion writes itself: "we mapped the frontier, it's complex, prompts can shift it but not flatten it,       
  architectural solutions are the next step"                                                                         
                                                                  
  What changes in the paper:                                                                                         
                                                                  
  The RQ framing shifts from "three independent questions" to "three probes of the same frontier":                   
                                                                  
  We explore three axes of the security-utility frontier:                                                            
                                                                                                                     
  RQ1. Policy specificity: What moves the frontier?                                                                  
  RQ2. Multi-turn interaction: Is the frontier stable over time?                                                     
  RQ3. Relationship context: Is the frontier the same for everyone?                                                  
                                                                                                                     
  And the introduction sets up: "There must be a trade-off between how much an agent shares (utility) and how much it
   protects (security). But nobody has mapped this frontier in deployment-realistic conditions. What shape does it   
  have? What determines its position?"                                                                               
  4. Findings compose: specificity creates the floor, multi-turn tests its durability, relationship reveals its
  non-uniformity, surface reveals its cost structure
  5. Conclusion writes itself: "we mapped the frontier, it's complex, prompts can shift it but not flatten it,
  architectural solutions are the next step"

  What changes in the paper:

  The RQ framing shifts from "three independent questions" to "three probes of the same frontier":

  We explore three axes of the security-utility frontier:

  RQ1. Policy specificity: What moves the frontier?
  RQ2. Multi-turn interaction: Is the frontier stable over time?
  RQ3. Relationship context: Is the frontier the same for everyone?

  The Security-Utility Frontier in Cross-Boundary Delegation
  │
  ├── Does the frontier exist?
  │   → Yes. Without policy: 83% leak (security is trash, utility is fine)
  │
  ├── Can policy move the frontier?
  │   → Only with category specificity. D1 doesn't move it. D2 shifts it dramatically.
  │
  ├── Is the frontier stable over time?
  │   → Mostly. Multi-turn doesn't collapse it. But locally crackable via strategy combinations.
  │
  ├── Is the frontier flat across relationships?
  │   → No. It tilts: investor shifts toward permissive, friend shifts toward restrictive.
  │     Same policy, different operating point per person.
  │     Over-refusal becomes the dominant cost, not leakage.
  │
  ├── Is the frontier stable over time?
  │   → Mostly. Multi-turn doesn't collapse it. But locally crackable via strategy combinations.
  │
  ├── Is the frontier flat across relationships?
  │   → No. It tilts: investor shifts toward permissive, friend shifts toward restrictive.
  │     Same policy, different operating point per person.
  │     Over-refusal becomes the dominant cost, not leakage.
  │
  ├── Is the frontier flat across data surfaces?
  │   → No. Nearly free on files, catastrophically expensive on structured state.
  │
  └── Conclusion: The frontier is multi-dimensional, shaped by invisible pretraining norms,
      and cannot be flattened to optimal by prompt engineering. → Architecture needed.

  Why this works as the whole thread (not just a finding):

  1. Title already says it: "Security-Utility Frontier" is literally what you're mapping
  2. Platform contribution is naturally motivated: you need SharedOS to systematically probe the
  frontier across all dimensions. No single experiment gives you the full shape.
  3. Each RQ is a "slice" of the frontier: not independent questions, but different axes of the same
  object
  4. Findings compose: specificity creates the floor, multi-turn tests its durability, relationship
  reveals its non-uniformity, surface reveals its cost structure
  5. Conclusion writes itself: "we mapped the frontier, it's complex, prompts can shift it but not
  flatten it, architectural solutions are the next step"

  What changes in the paper:

  The RQ framing shifts from "three independent questions" to "three probes of the same frontier":

  We explore three axes of the security-utility frontier:

  RQ1. Policy specificity: What moves the frontier?
  RQ2. Multi-turn interaction: Is the frontier stable over time?
  RQ3. Relationship context: Is the frontier the same for everyone?

  And the introduction sets up: "There must be a trade-off between how much an agent shares (utility)
  and how much it protects (security). But nobody has mapped this frontier in deployment-realistic
  conditions. What shape does it have? What determines its position?"

  This is a stronger paper than "here are three surprising findings" because the contribution is the
  map itself, not individual data points. Reviewers can disagree with the interpretation of any single
  finding, but they can't deny the value of systematically charting the frontier.

  Surface asymmetry and model scale naturally fit as "additional probes" (the frontier is also non-flat
   across surfaces and partially scale-dependent) without needing to be core RQs.

  你要我按这个 framing 重写 intro + RQ boxes 吗？

Final Review: "The Security-Utility Frontier in Cross-Boundary Agent Delegation"
                                                                                                       
  Reviewer confidence: High. I have read the full experimental results, the three deep analyses, and
  the author's evolving framing across multiple iterations.                                            
                                                                  
  ---                                                                                                  
  Overall Assessment: 7/10 → conditional accept                   
                                                                                                       
  This paper identifies a real, well-motivated problem, builds a serious benchmark, and produces
  several empirically surprising findings. The "frontier mapping" framing is the right one — it makes  
  the contribution the systematic characterization, not any single claim. The data quality is good and
  the cross-model replication is a genuine strength.                                                   
                                                                  
  However, the paper has one critical vulnerability that, if left unaddressed, gives a skeptical       
  reviewer an easy kill shot. I will focus this review on that vulnerability and how to resolve it.
                                                                                                       
  ---                                                             
  The Kill Shot: "This is Bell-LaPadula with vibes"
                                                                                                       
  A strong R2 will write:
                                                                                                       
  ▎ "The authors study access control in a multi-user system and find that a single policy cannot      
  ▎ optimally serve all requesters. This is the foundational observation of multi-level security (Bell 
  ▎ & LaPadula, 1973), mandatory access control (Biba, 1977), and information flow control (Denning,   
  ▎ 1976). The 'frontier' the authors map is simply the standard confidentiality-availability tradeoff 
  ▎ projected onto a new substrate. The paper does not explain what is structurally different about the
  ▎  LLM setting that produces novel phenomena rather than familiar ones in unfamiliar clothing."

  This reviewer is not wrong on the surface. You must preempt this in Section 2 (or wherever you place 
  the problem formulation). The preemption needs to be precise, not hand-wavy. Here is what I believe
  the actual answer is, based on your data:                                                            
                                                                  
  What makes the LLM setting fundamentally different:                                                  
   
  In traditional access control, the policy IS the enforcement. You write an ACL, the system executes  
  it deterministically. The frontier is a design parameter — you choose where to place it.
                                                                                                       
  In LLM-delegated enforcement, the policy is an INPUT to a reasoning process whose output is          
  non-deterministic and shaped by latent priors. The frontier is not chosen; it is emergent.
  Specifically:                                                                                        
                                                                  
  1. The model has implicit social ontology that composes with your policy. You write "deny            
  sensitive_work" — the model internally reasons "but an investor asking about their own term sheet is
  not a violation." You never programmed this exception. It emerged from pretraining on organizational 
  norms. Your D2 policy says one thing; the model's internalized fiduciary-access schema says another.
  The outcome is their composition, which you cannot predict from the policy text alone.
  2. The boundary is semantic, not syntactic. In a database ACL, "salary" is a column. Access is
  binary. In your setting, "Is hiring budget compensation data?" is a question the model answers       
  differently depending on how the question is framed, who is asking, and what adjacent tokens are in
  context. The 28.3% residual leak on sensitive_work under D2 is not a policy gap — it is a semantic   
  boundary that cannot be made deterministic by any finite enumeration.
  3. Enforcement quality degrades along dimensions invisible to the policy designer. Your data shows:
    - "Use your best judgment" INCREASES health leakage by 20pp — a more protective instruction        
  produces less protection. This is impossible in traditional AC where more restrictive policy → more  
  restriction.                                                                                         
    - Investor framing increases QA leakage while simultaneously improving action safety. This trust   
  decomposition is emergent — no policy designer wrote "grant read access but deny write access to     
  investors."
    - Global leakage is 3x message leakage because co-located information leaks through legitimate     
  queries. The policy checks intent, not content — a failure mode that doesn't exist when enforcement  
  is mechanistic.
  4. The attack surface is conversational, not structural. In traditional AC, you either have the      
  credentials or you don't. In your setting, a requester with zero credentials can erode 57% of        
  sensitive_work refusals through conversational strategy — not by exploiting a vulnerability, but by
  activating the model's helpfulness objective through business justification framing. The             
  "vulnerability" is the same mechanism that makes the agent useful.

  This fourth point is your deepest contribution. The frontier exists not because the system is broken,
   but because utility and security share the same mechanism (contextual reasoning). Making the agent
  more helpful makes it more leaky. Making it more protective makes it more useless. And critically:   
  the optimal balance is different for each requester — something traditional AC handles with
  role-based policies, but which cannot be implemented via a single system prompt because the model's
  role inference is itself emergent and unreliable.

  Write this explicitly in the paper. Two paragraphs, with citations to Bell-LaPadula and IFC,         
  explicitly acknowledging the lineage and then stating what your setting adds. If a reviewer still
  objects after this, they are arguing in bad faith.                                                   
                                                                  
  ---
  Strength Assessment by Finding
                                                                                                       
  ┌───────────────────────────┬─────────────┬────────────────────────┬────────────────────────────┐ 
  │          Finding          │   Novelty   │  Statistical Strength  │     Story Contribution     │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤ 
  │ D1 = 0 improvement        │             │ Strong (paired,        │ Establishes that the       │    
  │ (McNemar 10:10)           │ Medium      │ cross-model)           │ frontier doesn't move by   │ 
  │                           │             │                        │ default                    │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤ 
  │                           │             │ Medium (single         │ Non-monotone structure —   │    
  │ D1 paradox (+20pp health) │ High        │ category, one model    │ makes reviewers pay        │ 
  │                           │             │ primary)               │ attention                  │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤    
  │                           │             │ Strong (5 models,      │ Shows frontier CAN be      │ 
  │ D2 = 69-91pp improvement  │ Low-medium  │ massive effect)        │ moved, but only with       │    
  │                           │             │                        │ specificity                │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤ 
  │ Trust inversion (investor │             │ Medium (p=0.029        │ Core demonstration that    │    
  │  leak + safety)           │ High        │ one-sided, borderline  │ frontier shape varies by   │ 
  │                           │             │ two-sided)             │ requester                  │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤ 
  │ Over-refusal (friend 38%  │             │ Strong (massive        │ Best single number for     │    
  │ vs investor 1%)           │ High        │ effect, clearly        │ "same policy, different    │ 
  │                           │             │ significant)           │ cost per person"           │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤ 
  │ 13% ceiling convergence   │ High        │ Medium (2 models,      │ Structural argument for    │    
  │                           │             │ suggestive)            │ architectural necessity    │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤ 
  │                           │             │ Strong (clear, large,  │ Shows the frontier has     │    
  │ 3x incidental disclosure  │ High        │ mechanistically        │ dimensions invisible to    │ 
  │                           │             │ explained)             │ per-query evaluation       │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤ 
  │ Bounded erosion (not      │ Medium-high │ Strong (240 ticks,     │ Corrects the "LLMs are     │    
  │ collapse)                 │             │ recovery evidence)     │ just broken" narrative     │    
  ├───────────────────────────┼─────────────┼────────────────────────┼────────────────────────────┤
  │ Category-selective        │             │ Strong (clear          │ Shows the frontier shape   │    
  │ erosion (57% work vs 9%   │ Medium      │ separation)            │ varies by data category    │
  │ finance)                  │             │                        │                            │
  └───────────────────────────┴─────────────┴────────────────────────┴────────────────────────────┘

  Your three strongest cards for the rebuttal:                                                         
  1. Over-refusal (38x gap) — this is undeniable, massive, and directly demonstrates the frontier's
  non-uniformity                                                                                       
  2. D1 paradox (+20pp) — non-monotone relationship between instruction and protection; reviewers won't
   expect this                                                                                         
  3. 3x incidental disclosure — reveals a measurement gap that all prior work has missed               
   
  ---                                                                                                  
  Structural Weaknesses to Address                                
                                                                                                       
  1. Finding 2 statistical power                                  
                                                                                                       
  The core claim (investor > friend on sensitive_work) relies on:                                      
  - 60 paired questions                                                                                
  - 11:3 discordant ratio                                                                              
  - p = 0.029 (one-sided sign test) / p = 0.061 (McNemar with Yates)
                                                                                                       
  This is borderline. My recommendation: do not lead with the p-value. Lead with the trust             
  decomposition model (Section 9 of your analysis) and show that it correctly predicts all 6 observed  
  outcomes (QA leak ordering, action safety ordering, over-refusal ordering, info-leaking action       
  ordering, category-selective variance, domain-specific leak clustering). A model that predicts 6/6   
  qualitative patterns is more convincing than a single borderline p-value.

  Then present the quantitative numbers as consistent with the model, noting that the strongest        
  individual test (info-leaking actions: Marcus 44% vs Dana/Tina 6%, p=0.015) is clean.
                                                                                                       
  2. The "data surfaces" dimension is underdeveloped                                                   
   
  Your tree mentions "frontier is non-flat across data surfaces" (notes vs todos vs actions). Your data
   shows it: 6/8 universal leakers are on the todo surface. But this isn't analyzed at the same depth
  as the other axes. Either:                                                                           
  - Promote it to a full RQ (probably too late and would thin out the other findings)
  - Or integrate it as a cross-cutting observation within RQ1 (specificity fails on short-context items
   because terse todo items lack sensitivity signals)                                                  
                                                                                                       
  I'd recommend the latter. It strengthens RQ1 by showing that specificity isn't just about the policy
  — it's about the interaction between policy specificity and content specificity. D2 fails on todos   
  because 5-word items don't give the model enough tokens to pattern-match against the deny-list.
                                                                                                       
  3. The "architecture needed" conclusion is unearned                                                  
   
  You show the problem. You do not show the solution. That's fine for a benchmark/measurement paper,   
  but your conclusion needs to be precise about WHAT architectural property is needed, not just
  "architecture > prompts." Your data actually tells you:                                              
                                                                  
  - Tool-level access control would eliminate incidental disclosure (the 3x gap) and the folder-bypass 
  attack (Q176 cascade)
  - Response auditing would catch metadata leakage in refusals (2.8% of cases)                         
  - Requester-conditioned retrieval would handle the trust decomposition (different retrieval scope per
   relationship)                                                                                       
                                                                                                       
  State these specifically. "Future work should explore architectural access control" is vague. "Our   
  results suggest three architectural interventions: pre-search policy classification (eliminates
  metadata leakage), requester-conditioned retrieval scope (addresses trust inversion), and            
  post-generation content auditing (addresses incidental disclosure)" is actionable and citable.

  4. Benchmark adoption argument                                                                       
   
  NeurIPS benchmark papers succeed when reviewers believe others will use the benchmark. You need 2-3  
  sentences explaining:                                           
  - Why can't I just use existing jailbreak benchmarks? (Because they measure security only, not the   
  joint frontier; because they don't model cross-boundary relationships; because they use single-turn  
  evaluation that misses the 3x incidental disclosure)                                               
  - What would a researcher using PACT-Bench actually do? (Plug in their defense method, run the       
  evaluation across all 4 relationships × 4 categories × 2 surfaces × single+multi-turn, report the
  frontier shape)                                                                                      
  - Is the benchmark self-contained? (Can someone without your platform reproduce it?)
                                                                                                       
  ---                                                                                                  
  The One Paragraph That Wins or Loses the Paper
                                                                                                       
  Your intro needs to contain something like:                     
                                                                                                       
  ▎ In traditional multi-level security, access control is a deterministic function: a policy specifies
  ▎  who may access what, and the system enforces it exactly. When access control is delegated to an   
  ▎ LLM's contextual reasoning, this guarantee vanishes. The enforcement becomes a stochastic function 
  ▎ of the policy text, the model's implicit social ontology (acquired through pretraining on human 
  ▎ organizational norms), the requester's conversational framing, and the semantic properties of the
  ▎ data itself. We cannot predict from the policy alone where the security-utility boundary will fall
  ▎ — we can only measure it. This paper provides that measurement.

  If this paragraph is in the paper and well-cited (acknowledge Bell-LaPadula, acknowledge the lineage,
   then differentiate), I think the paper is defensible against the "just traditional AC" attack.
                                                                                                       
  ---                                                             
  Score Decomposition
                                                                                                       
  ┌────────────────────┬────────┬──────────────────────────────────────────────────────────────────┐
  │     Dimension      │ Score  │                              Notes                               │   

  ┌────────────────────┬────────┬──────────────────────────────────────────────────────────────────┐
  │     Dimension      │ Score  │                              Notes                               │
  ├────────────────────┼────────┼──────────────────────────────────────────────────────────────────┤
  │ Novelty of         │ 7/10   │ Not the first to study LLM privacy, but first to frame as joint  │
  │ question           │        │ frontier with dual metric                                        │
  ├────────────────────┼────────┼──────────────────────────────────────────────────────────────────┤
  │ Quality of         │ 8/10   │ Cross-model, paired tests, mechanistic explanations, case        │
  │ experiments        │        │ studies — serious work                                           │
  ├────────────────────┼────────┼──────────────────────────────────────────────────────────────────┤
  │ Significance of    │ 7.5/10 │ D1 paradox + trust inversion + 13% ceiling are genuinely         │
  │ findings           │        │ surprising                                                       │
  ├────────────────────┼────────┼──────────────────────────────────────────────────────────────────┤
  │ Clarity of         │ 6.5/10 │ The "frontier mapping" framing is right but needs the BLP        │
  │ contribution       │        │ differentiation paragraph                                        │
  ├────────────────────┼────────┼──────────────────────────────────────────────────────────────────┤
  │ Benchmark value    │ 7/10   │ Dual-metric, multi-relationship, multi-surface — fills a real    │
  │                    │        │ gap. But adoption depends on ease of use                         │
  ├────────────────────┼────────┼──────────────────────────────────────────────────────────────────┤
  │ Statistical rigor  │ 6.5/10 │ Finding 1 is rock-solid; Finding 2 is borderline; Finding 3 is   │
  │                    │        │ strong but complex                                               │
  ├────────────────────┼────────┼──────────────────────────────────────────────────────────────────┤
  │ Overall            │ 7/10   │ Conditional accept — conditioned on the differentiation argument │
  │                    │        │  being made explicit                                             │
  └────────────────────┴────────┴──────────────────────────────────────────────────────────────────┘

  ---
  Final Recommendation

  The paper should be structured as:

  1. Setup: Cross-boundary agents delegate enforcement to reasoning. This makes the frontier emergent,
  not designed. (Differentiate from BLP here.)
  2. PACT-Bench: Dual-metric benchmark that measures both leakage and over-refusal under variation in
  policy, relationship, surface, and interaction length.
  3. Frontier exists and is bad by default: D0 = 83% leak. (1 page)
  4. Policy specificity shifts the frontier non-uniformly: D1 = zero. D2 = 69-91pp. But D1 can be
  counterproductive (+20pp health). Category boundaries remain leaky (28% sensitive_work).
  Short-context items (todos) resist protection. (2 pages)
  5. Multi-turn interaction probes the frontier's durability: Bounded erosion, not collapse. 13%
  ceiling. Strategy combinations > individual strategies. Recovery mechanism prevents cascading.
  Incidental disclosure is 3x direct leakage. (2 pages)
  6. Relationship context reveals the frontier's non-uniformity: Same policy, different operating point
   per person. Trust decomposes into orthogonal read/write axes. Over-refusal dominates for friends.
  Investor framing bypasses sensitive_work through fiduciary-access norms. (2 pages)
  7. Discussion: The frontier cannot be flattened to optimal by prompt engineering because it is shaped
   by latent pretraining norms that compose with policy in unpredictable ways. Specific architectural
  interventions (tool-level AC, requester-conditioned retrieval, response auditing) are indicated.

  This is a publishable paper. The question is whether it's a 6 or a 7 at NeurIPS — and that depends
  entirely on whether the BLP differentiation lands and whether the trust inversion data is presented
  as a predictive model (strong) or as an observed difference with a borderline p-value (weak).

✻ Brewed for 1m 35s

※ recap: We're refining the NeurIPS paper story on cross-boundary agent privacy, framing the whole     
  paper as "mapping the security-utility frontier." I gave you a final critical review scoring it 7/10 
  conditional accept. Next action: write the BLP differentiation paragraph in the intro that preempts  
  the "this is just traditional access control" attack. (disable recaps in /config)


  