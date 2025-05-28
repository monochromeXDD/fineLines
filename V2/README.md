this will be the second working (prototype for my project):

16.05.2025
objectives/expected improvements over V1:

1. better dB organization
2. multiple PDFs persistence
3. separate mechanism for:
      - pdf uploading and embedding
      - & the chatbot interface
4. performance enhacements
  - similar model
  - better prompt template
  - adding a confidence metric 
  - expermenting with chunk size and overlapping
  - other unknown methods yet
5. token streaming
6. a workable UI using StreamLit

19.05.2025
most of the above objectives have been achieved. next objectives:
1. add contextual memory in-chat: a back-and-forth conversational styled understanding to be able to answer follow-up questions.
2. adding a cofidence metric (didnt add it in the previous update)
3. further performance enhancements needed - too slow rn dawg, even with mistral-instruct-7b; maybe it's just my lazy ass laptop
5. option for the user to download the current session chats
6. aesthetic improvements maybe?

P.S: this will all still be local

22.05.2025
1. added contextual memory: back and forth conversation styles chat
2. confidence metric and current session chat downloaded not implemented rn
3. created the API version of the same fineLines but emplying API for faster inference (groqAPI)
      - too slow on local running even with QWEN3.3:0.6B (i.e, 0.6B parameters, the most lightweight and fastest i could find currently available)
  
28.05.2025
1. was tasked with adding a userAuth checkpoint for enabling admin-only access of the dB.
2. using google cloud's OIDC (OAuth2) platform (testing phase, local deployment), i am successful in implmenting authentcation but no roles-based autherization.
3. in my observation, a fully fledged roles based authentication will be possible with a full revamp of the fineLines structure but keeping the core RAG functionalities intact.
4. Based on this, i am now shifting my effort towards the developemnet of fineLines V3.
