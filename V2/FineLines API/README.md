version equivalent to V2 but employs groq API so it's much faster

file with the API key has not been uploaded for obvious reasons 


this will be the second working (prototype for my project):

16.05.2025 objectives/expected improvements over V1:

better dB organization
multiple PDFs persistence
separate mechanism for:
pdf uploading and embedding
& the chatbot interface
performance enhacements
similar model
better prompt template
adding a confidence metric
expermenting with chunk size and overlapping
other unknown methods yet
token streaming
a workable UI using StreamLit
19.05.2025 most of the above objectives have been achieved. next objectives:

add contextual memory in-chat: a back-and-forth conversational styled understanding to be able to answer follow-up questions.
adding a cofidence metric (didnt add it in the previous update)
further performance enhancements needed - too slow rn dawg, even with mistral-instruct-7b; maybe it's just my lazy ass laptop
option for the user to download the current session chats
aesthetic improvements maybe?
P.S: this will all still be local

22.05.2025

added contextual memory: back and forth conversation styles chat
confidence metric and current session chat downloaded not implemented rn
created the API version of the same fineLines but emplying API for faster inference (groqAPI)
too slow on local running even with QWEN3.3:0.6B (i.e, 0.6B parameters, the most lightweight and fastest i could find currently available)
28.05.2025

was tasked with adding a userAuth checkpoint for enabling admin-only access of the dB.
using google cloud's OIDC (OAuth2) platform (testing phase, local deployment), i am successful in implmenting authentcation but no roles-based autherization.
in my observation, a fully fledged roles based authentication will be possible with a full revamp of the fineLines structure but keeping the core RAG functionalities intact.
Based on this, i am now shifting my effort towards the developemnet of fineLines V3.
Imp points: all further developement for fineLines will work on API based LLM inference as it is much more faster to work with, test, and can be easily scaled in the future if required.
