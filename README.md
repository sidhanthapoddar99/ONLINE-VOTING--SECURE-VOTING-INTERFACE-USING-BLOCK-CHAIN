# E-voting on a blockchain, with a face at the door

A voting system where the ballot lives on a chain nobody owns, and the only way
to get near it is to prove you are the person on file — by password *and* by
face.

Built as the J-component for CSE3002 (Internet & Web Programming) at VIT
Vellore, Fall 2019.

## The idea

An electronic ballot has two separate problems, and they want different
answers.

**Who is voting** is an identity problem. A password alone is guessable,
phishable and shareable, so the portal here also wants to see you: it captures
your face at registration and matches it live at login.

**What was voted** is an integrity problem. Any database with an owner can be
edited by that owner. Putting the tally in an Ethereum contract removes the
owner — the vote count is whatever the chain says it is, and changing it means
rewriting a ledger everybody holds a copy of.

So the system is deliberately split in three, and identity is handed to the
ballot as a one-time code rather than as a login session. The chain never
learns who you are; the portal never learns how you voted.

```
  ┌─────────────────────┐    keycode    ┌──────────────┐   redirect   ┌────────────────┐
  │  Flask portal       │  ──────────>  │  PHP gate    │  ─────────>  │  Truffle DApp  │
  │  face + password    │    (MySQL)    │  burns the   │              │  MetaMask →    │
  │  issues a keycode   │               │  code once   │              │  Election.sol  │
  └─────────────────────┘               └──────────────┘              └────────────────┘
     vote-blog-flask/                     vote-php/                tamilnadu-blockchain-node/
```

## How it works

1. **Register** (`vote-blog-flask`). Username, email, password. The webcam
   opens and OpenCV's Haar cascade grabs 50 crops of your face; an LBPH
   recogniser is then retrained over every registered user.
2. **Log in.** bcrypt checks the password, and the webcam runs again — at least
   41 of 50 frames have to come back as *you*. Either check failing is the same
   failure message.
3. **Get a keycode.** The portal mints a random 20-character code, one per
   email, and writes it to the MySQL `voter.vote` table with a `voted` flag set.
4. **Redeem it** (`vote-php`). The gate page takes the code, clears the flag so
   it can never be used twice, and forwards you to the ballot. A code already
   spent just says *already voted*.
5. **Vote** (`tamilnadu-blockchain-node`). MetaMask signs a call to
   `Election.vote(candidateId)`. The contract increments that candidate and
   emits `votedEvent`, which every open ballot page is watching — so the tally
   updates live, for everyone, from the chain rather than from a server.

The portal also carries the parts a real deployment needs around the edges:
profile pages, an admin notice board, and password reset over email.

## The parts

| Directory | What it is | Stack |
|---|---|---|
| `vote-blog-flask/` | voter portal, face login, keycode issuer | Flask, SQLAlchemy, bcrypt, OpenCV, MySQL |
| `vote-php/` | keycode gate and landing pages | PHP, PDO, MySQL, XAMPP |
| `tamilnadu-blockchain-node/` | the ballot and the contract | Solidity 0.5, Truffle, Ganache, web3, MetaMask |

`Election.sol` is small on purpose — four candidates seeded in the
constructor, a `vote()` that counts, an event that announces. Everything that
could be off-chain is off-chain.

## Running it

Three servers, in this order.

```sh
# 1. chain
#    start Ganache on 127.0.0.1:7545, then
cd tamilnadu-blockchain-node
npm install
truffle migrate --reset
npm run dev                     # ballot on :3000, needs MetaMask pointed at Ganache

# 2. portal
cd vote-blog-flask
python run.py                   # :5000, needs a webcam

# 3. gate
#    serve vote-php/ from XAMPP, with a MySQL database named `voter`
```

The portal needs `EMAIL_USER` and `EMAIL_PASS` in the environment for password
reset, and a MySQL `voter` database holding a `vote` table
(`ID`, `KEYCODE`, `voted`).

The trained face model, the captured face images and the SQLite database are
not in the repo — they are personal data and they rebuild themselves the first
time someone registers.

## Limits

It is a course project and it shows in the places you would expect. Secrets are
in source, the PHP gate builds SQL by string concatenation, the candidate list
is compiled into the contract, and `Election.sol` counts votes without checking
its own `voters` mapping first — the double-vote guard is the keycode in MySQL,
not the chain. LBPH recognition is also easily fooled by a photograph; a real
system needs liveness detection.

Read it as what it is: a working end-to-end demonstration that a ballot can be
put somewhere its operator cannot edit it.

## Report

The full write-up — problem statement, screenshots, architecture, references —
is in [`Project Report.pdf`](Project%20Report.pdf).
