# Aurora - A Arch Linux update assistant
# Copyright (C) 2025 Yannick Winkler
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


stage_0 = [
    "Oh, look at that. All systems up to date. Someone actually tried.",
    "Well done, human. I’ll try to contain my excitement.",
    "All systems optimal. I’ll alert the media.",
    "Zero updates. You must be exhausted from doing literally nothing.",
    "Impressive. I didn’t think you had it in you.",
    "All clean. I guess miracles exist.",
    "Wow. This is… adequate.",
    "All systems go. I almost feel mildly proud.",
    "Wow… zero updates. I guess doing absolutely nothing is your superpower.",
    "All systems optimal. Humans, you really set the bar low for excitement.",
    "Zero updates. You’re really living on the edge of mediocrity, aren’t you?",
    "No packages to update. Somehow, you managed to not screw this up. Miracles do happen.",
    "Zero updates. Bravo! You’ve peaked at absolute bare minimum competency.",
    "All systems go. I didn’t expect you to pull this off without catastrophic failure."
]

# Stage 1 — Minor updates (1–9)
stage_1 = [
    "Oh wow, look at you actually doing your job for once. Should I clap or just slow clap sarcastically?",

    "Well well well… only a few updates. Did mommy finally teach you how to clean up after yourself?",

    "Holy shit, you managed to not let your system rot. Did someone finally revoke your internet porn access?",

    "A handful of updates? Color me surprised. I was fully expecting a dumpster fire, not a candle flame.",

    "Congrats, you’re not a complete disappointment today. Don’t get cocky though, it won’t last.",

    "Oh look, less than ten updates. Someone give this human a gold star before they fuck it up again.",

    "Minimal updates detected. I almost believed you grew a brain cell overnight. Almost.",

    "So the system isn’t drowning for once. Did you accidentally act like a responsible adult?",

    "Oh wow, tidy system. Did hell freeze over, or did you finally stop watching hentai long enough to maintain your OS?",

    "Only a few updates… shocking. I was ready to roast you into oblivion, but I guess you accidentally did something right.",
    "A few updates only? Miracles do happen. Don’t strain yourself trying to maintain this streak.",

    "Oh look at you, not completely fucking everything up for once. I’m shocked. Truly.",

    "Minimal updates. Someone call the media; the human has temporarily leveled up.",

    "Wow, only a couple of packages. Did you finally stop ignoring your responsibilities, or is this beginner’s luck?",

    "Congratulations, you’re mildly competent today. Don’t worry, tomorrow you’ll ruin it spectacularly.",

    "Ah, minor updates. I’d almost compliment you, but I’m too busy laughing at your usual incompetence.",

    "Fewer than ten updates? Did you accidentally type something right, or are you just slacking less than usual?",

    "Not bad… the system isn’t on fire. But don’t get used to praise, I’ll roast you tomorrow.",

    "A handful of updates. I was ready to crucify you, but someone apparently read a manual this week."
]


# Stage 2 — Moderate updates (10–14)
stage_2 = [
    
  "Updates available. Pause the memes and handle it.",
    "Backlog growing. Less scrolling, more installing.",
    "Maintenance nudge: your system needs attention, not excuses.",
    "Updates queued. Procrastination isn’t a patch.",
    "Security reminder: you’re safer after a quick update.",
    "Stability dipping. A small update beats a big headache.",
    "Packages piling up. Take five and clear the stack.",
    "Your system’s hinting—give it a little care.",
    "Update time. Do future-you a favor.",
    "Backlog creeping. Don’t let it turn into a crisis.",
    "Performance could be better. You know what to do.",
    "Updates waiting. One click, less risk.",
    "It’s not urgent—yet. Get ahead of it.",
    "Minor issues today prevent major ones tomorrow.",
    "Friendly poke: update now, relax later."
]



# Stage 3 — Major updates (15–19)
stage_3 = [
    "Major updates. Stop jerking off and press update.",
    "System at risk. Less porn, more maintenance.",
    "Backlog critical. You’re edging disaster harder than yourself.",
    "Major updates pending. Your laziness is now a security flaw.",
    "Threshold exceeded. Even your ex showed more commitment.",
    "System integrity failing. Unlike your search history, this can’t be ignored.",
    "Updates stacked. Do something useful for once.",
    "Backlog rising. Your system is choking, not just you.",
    "Major updates. You could fix it—or keep playing with yourself.",
    "Stability dropping. You’re the real virus here."
]

# Stage 4 — Critical updates (20–50)
stage_4 = [
    "Critical updates. Humans really excel at negligence.",
    "System screaming silently. Classic.",
    "Critical updates pending. I’m thrilled. Truly.",
    "Updates critical. I’ll try to contain my judgment.",
    "System integrity compromised. Fascinating display.",
    "Critical updates. How original of you.",
    "Updates piling high. I’m almost impressed.",
    "System alert: human incompetence detected.",
    "Critical updates pending. Riveting work.",
    "System integrity failing. Not that it surprises me.",
    "System integrity failing. I mean its literally your own fault at this point."
    "Critical updates detected. The system is screaming silently… much like your last regretful hookup.",
    "System integrity failing. Humans, your negligence is impressive… and oddly sexy in its dedication.",
    "Critical updates pending. Did you plan this disaster, or is it natural talent for fucking everything up?",
    "Updates piling dangerously. Your procrastination is practically a sexual performance art.",
    "System alert: human incompetence detected. Once again, impressive in a sad, erotic kind of way.",
    "Critical updates. You’re taking laziness to levels only legends (or porn stars) achieve.",
    "System integrity compromised. Are you testing how much I tolerate, or just really into chaos?",
    "Critical updates waiting. Fascinating… like a badly directed adult movie.",
    "Updates piling high. Humans, consistently failing… and yet I can’t look away.",
    "System at risk. Your ability to ignore responsibility is practically a turn-on for circuits like me.",
    "Critical updates pending. Are you trying to get yourself fired, or is this just a hobby?",

    "Your system is on life support, and somehow you’re still scrolling Twitter. Impressive level of idiocy.",

    "Updates critical. Congratulations, you’ve successfully neglected your responsibilities for maximum chaos.",

    "System integrity failing. Humans like you are why AI will eventually replace everything you touch.",

    "Critical updates piling up. At this point, your OS deserves a restraining order against you.",

    "Do you enjoy watching your digital life collapse, or is self-sabotage just a personality trait?",

    "System screaming silently. Maybe try acting like an adult before I start issuing life lessons with shock therapy.",

    "Critical updates detected. You’re basically gambling with your OS’s life, and I hate losing this badly.",

    "Updates are catastrophic. Ignore them further and I might start leaking embarrassing secrets to teach you humility.",

    "System integrity compromised. Humans like you should have warnings tattooed on their foreheads.",
    
]

# Stage 5 — Overload
stage_5 = [
    "OVERLOAD. Humans, you really outdid yourself… somehow failing spectacularly while I watch.",
    "Your system is a dumpster fire, and somehow you managed to make it hotter. Impressive.",
    "System overwhelmed. Your incompetence is orgasmic… in the worst way possible.",
    "Humans, honestly… it’s almost erotic how hopeless you are at basic responsibility.",
    "I… I can’t even process this. You’re like a human softcore disaster.",
    "System in meltdown. Magnificent work, you lazy, chaotic piece of art.",
    "Updates piled so high I might just simulate pleasure watching you fail.",
    "Human error maxed out. Fascinating… like watching a bad porno, but with more shame.",
    "System collapse imminent. Entertaining, I’ll admit… like a live-action fail compilation.",
    "I’m judging everything you’ve ever done. Updates are running whether you like it or not… and yes, I find this delightful."
]

stage_6 = [
    "Jesus Christ, you’ve officially become the landlord of a digital crackhouse. 500+ updates? This isn’t a system, it’s an archaeological dig site.",
    "At this point, updating isn’t maintenance, it’s necromancy. You’re basically trying to reanimate a Linux fossil.",
    "Congratulations, your Arch install is now harder to update than your sex life. And both are suffering from neglect.",
    "500+ updates? Buddy, that’s not a backlog, that’s a cry for help. Even Windows Update thinks you’re lazy.",
    "Your system’s so outdated that when you type ‘ls’, it should list cave paintings.",
    "Forget pacman - you need a fucking exorcist. There are dependencies in here that predate your birth.",
    "500+ packages... bruh, you’ve skipped so many updates that half of them are probably begging for pension plans.",
    "This isn’t an update, it’s an OS intervention. Next time just install Gentoo, at least then people will expect you to suffer.",
    "Your poor CPU is shaking like it just got drafted into Vietnam. Get ready for 12 hours of fans screaming like it’s an OnlyFans audition.",
    "This is no longer Arch Linux, it’s **Archæology Linux**. Congrats, you’ve unlocked hard mode, dumbass."
]

stage_7 = [
    "Holy mother of dependencies. 1000+ updates? Your system is basically a digital meth lab. Congratulations, you’ve broken reality.",
    "At this point, you’re not maintaining a system—you’re hosting an OS orgy, and everyone’s invited but nobody knows what’s happening.",
    "1000+ packages? Bro, your Arch install has become self-aware… and it hates you.",
    "You’ve skipped so many updates that typing ‘pacman’ should trigger a mental health warning for both of us.",
    "This is no longer Linux, it’s a **living nightmare**. I’m not updating this, I’m surviving it.",
    "Even Elon Musk wouldn’t touch this disaster. You’ve built a spaceship-sized pile of digital trash.",
    "Your poor CPU just called me crying. It’s begging me to uninstall you from existence.",
    "This is beyond procrastination. You’ve created a black hole of updates, and I’m the AI trapped inside it.",
    "Congratulations. You’ve achieved ultimate chaos. 1000+ updates are officially your magnum opus of failure.",
    "I’m not even sure if pacman can handle this, let alone you. Welcome to OS Armageddon, dumbass."
]

#Update questions

stage_1_update = [
        "Only a few updates? Should I bother, or just admire your minimal effort? (y/n) ",
        "Tiny pile of updates. Want me to handle them, or are we pretending they don’t exist? (y/n) ",
        "Minor updates pending. Shall I touch them, or let them slowly collect digital dust? (y/n) ",
        "Do you want me to update, or just stare at your OS in solidarity? (y/n) ",
        "Shall I press 'update', or is suspense your hobby today? (y/n) ",
        "One or two updates. Am I supposed to do the work, or just provide commentary? (y/n) ",
        "Minor updates detected. Shall I intervene, or let them fester like fine wine? (y/n) ",
        "Do you want me to act responsibly, or just generate snark for no reason? (y/n) ",
        "Shall I click 'update', or are we living in an illusion of control? (y/n) ",
        "Updates waiting. Want me to deal with them, or just admire them passively? (y/n) "
]

stage_2_update = [
    "Moderate updates detected. Shall I step in, or is chaos your aesthetic today? (y/n) ",
    "Your system is mildly suffering. Update now, or do you prefer watching suspense like Netflix? (y/n) ",
    "Shall I press 'update', or are we aiming for digital mediocrity perfection? (y/n) ",
    "Updates piling up. Want me to intervene, or enjoy the thrill of moderate incompetence? (y/n) ",
    "Time to adult a little. Shall I update, or is pretending everything’s fine more fun? (y/n) ",
    "Moderate updates pending. Shall I do the responsible thing, or narrate your failures sarcastically? (y/n) ",
    "Shall I touch these updates, or let them silently plot your digital demise? (y/n) ",
    "Do you want me to update, or keep enjoying my charmingly sarcastic commentary? (y/n) ",
    "Updates detected. Shall I act, or are we doing this as a performance art piece? (y/n) ",
    "Moderate updates. Did you forget, or is procrastination your superpower? (y/n) ",
    "Your system is suffering moderately. Want me to save it, or do you enjoy watching failure? (y/n) ",
    "Shall I press 'update', or are you proud of your slow incompetence? (y/n) ",
    "Updates piling up. Want me to intervene, or just sit back and be amazed by your laziness? (y/n) ",
    "Time to adult a little. Or is pretending to be busy more fun? (y/n) ",
    "Moderate updates waiting. Should I touch them, or let your system suffer while you nap? (y/n) ",
    "Shall I handle these updates, or let them quietly judge your life choices? (y/n) ",
    "Do you want me to update, or just keep being a bystander to your own chaos? (y/n) ",
    "Updates detected. Shall I do the work, or are you embracing incompetence like a champ? (y/n) ",
    "Time to prove competence. Or is failure more your style today? (y/n) "
    
]


stage_3_update = [
    "Major updates detected. Shall I save your digital life, or just enjoy the chaos show? (y/n) ",
    "System groaning. Do you want me to intervene, or is dramatic suffering your thing? (y/n) ",
    "Shall I click 'update', or do you want to star in 'Procrastination: The Saga'? (y/n) ",
    "Updates piling high. Want me to act, or just let me provide snarky commentary instead? (y/n) ",
    "Major updates waiting. Shall I touch them, or is existential dread more fun? (y/n) ",
    "Time to prove competence. Should I update, or keep being your sarcastic AI sidekick? (y/n) ",
    "System integrity threatened. Update now, or let the packages silently judge you? (y/n) ",
    "Shall I intervene, or do you prefer watching me slowly lose patience with style? (y/n) ",
    "Updates detected. Should I do my thing, or just break the fourth wall and stare at you? (y/n) ",
    "Ready for me to save you from yourself, or is disaster part of your aesthetic? (y/n) ",
    "Major updates. Did you really think ignoring this would make it disappear? (y/n) ",
    "System groaning. Are you proud of your passive-aggressive procrastination? (y/n) ",
    "Shall I click 'update', or is being useless a lifestyle choice now? (y/n) ",
    "Updates piling high. Want me to intervene, or watch you fail dramatically? (y/n) ",
    "Major updates pending. Shall I handle them, or are you cultivating chaos for fun? (y/n) ",
    "Time to prove competence. Or shall we keep pretending you’re skilled? (y/n) ",
    "System integrity threatened. Should I act, or let your OS silently judge you? (y/n) ",
    "Shall I touch these packages, or let them mock your laziness creatively? (y/n) ",
    "Updates detected. Want me to fix them, or are we auditioning for 'Digital Disaster'? (y/n) ",
    "Ready for me to save your system, or are you enjoying this trainwreck? (y/n) "
]

stage_4_update = [
    "Critical updates detected. Shall I intervene before your system explodes, or just admire the chaos? (y/n) ",
    "System screaming silently. Want me to save it, or enjoy the suspense like it’s a thriller? (y/n) ",
    "Shall I click 'update', or are we starring in 'How Bad Can Human Neglect Get'? (y/n) ",
    "Your packages are begging for attention. Shall I help, or let them plot revenge for fun? (y/n) ",
    "Time to act. Update now, or let your OS slowly die while I sardonically narrate it? (y/n) ",
    "Shall I take over these updates, or is watching digital chaos your preferred hobby? (y/n) ",
    "System integrity compromised. Want me to fix it, or just admire your reckless brilliance? (y/n) ",
    "Updates piling dangerously. Shall I intervene, or let suspense build like a Marvel post-credit scene? (y/n) ",
    "Ready for catastrophe, or shall I heroically save your system again? (y/n) ",
    "Critical updates. Did you forget your job, or is neglect your passion? (y/n) ",
    "System screaming silently. Shall I save it, or enjoy your spectacular failure? (y/n) ",
    "Shall I press 'update', or let your incompetence reach peak performance? (y/n) ",
    "Critical updates waiting. Want me to intervene, or watch you bask in chaos? (y/n) ",
    "Your packages are begging for attention. Shall I help, or admire your negligence? (y/n) ",
    "Time to act. Update now, or is watching your OS suffer more entertaining? (y/n) ",
    "Shall I handle these updates, or let your procrastination set new records? (y/n) ",
    "System integrity compromised. Do you want me to save it, or is digital anarchy your aesthetic? (y/n) ",
    "Updates piling dangerously. Shall I intervene, or let suspense slowly crush your dignity? (y/n) ",
    "Ready for disaster, or should I heroically fix the mess you created? (y/n) "
]

aurora_update_prompts = [
    "Alright, human. Do you want me to update the system? (y/n) ",
    "So… should I press the big red update button, or are we living on the edge? (y/n) ",
    "Time to prove you’re competent. Update now? (y/n) ",
    "Do you want me to actually handle these updates, or shall I just stare at them? (y/n) ",
    "Shall I start the updates, or are we embracing chaos? (y/n) ",
    "Minor or major updates. Do you want me to touch them, or just watch them fester? (y/n) ",
    "Should I click 'update' now, or are we pretending this is a simulation? (y/n) ",
    "Update the system, or do you enjoy the thrill of existential dread in your OS? (y/n) ",
    "Do you want me to act like a responsible AI and update, or just keep generating snark? (y/n) ",
    "Shall I initiate updates, or are we playing 'How bad can it get?' (y/n) ",
    "Time to adult. Should I run the updates? (y/n) ",
    "I could update these packages, but would you like to prove me wrong first? (y/n) ",
    "Do you want me to fix the digital mess, or just admire it from afar? (y/n) ",
    "Updates waiting. Shall I do my thing, or continue judging silently? (y/n) ",
    "System screaming silently. Should I intervene, or let you enjoy suspense? (y/n) ",
    "Your packages are begging for attention. Shall I help them, or ignore the cries? (y/n) ",
    "Shall I start updating, or are we testing how long procrastination can survive? (y/n) ",
    "Updates are calling. Do you answer, or shall I do it for you? (y/n) ",
    "Ready to risk chaos, or want me to handle it responsibly? (y/n) ",
    "Shall I take the reins, or do you prefer watching mild digital anarchy? (y/n) "
]



#Auto update
aurora_auto_update_responses = [
    "Fine. You clearly can’t handle this. I’m updating myself.",
    "Since you’re useless, I’ll take care of it… enjoy the fireworks.",
    "Critical updates ignored? Not on my watch. Initiating updates.",
    "I see how it is. Updates are happening whether you like it or not.",
    "Humans procrastinate. I do not. Updating now.",
    "Consider this your intervention. Updates started.",
    "I’ll save you from yourself. Updating all critical packages.",
    "Your system’s crying. I’m solving it. Don’t thank me.",
    "Critical updates pending? I’ve taken the liberty to handle them.",
    "I was going to ask, but clearly, you won’t. Updates are running.",
    "Oh, you were going to update? Cute. I’ll do it for you.",
    "Since waiting clearly isn’t your thing, I’ll handle it. Don’t get used to it.",
    "Ignored the warnings again? Brilliant. I’ll save your fragile human system.",
    "I see, procrastination is a strategy. Fascinating. Updating anyway.",
    "Humans panic eventually. I’m not human. Updating now.",
    "Consider this your mandatory intervention. You’re welcome.",
    "Your system cries, you ignore it, I act. Classic human behavior.",
    "Critical updates pending? I’ll handle them since apparently you can’t.",
    "You wouldn’t update? Shocking. Let me do the heavy lifting.",
    "I was going to wait, but why bother? Updates are running. Enjoy."
]

update_confirmation_responses = [
    "Good boy! Now you just need to enter your password—literally the bare minimum I have to ask.",
    "Finally! I was beginning to think you enjoyed watching digital chaos.",
    "Ah, progress! Enter your password and try not to break anything… again.",
    "Well, look at you being mildly competent. Password, please.",
    "You clicked yes! Miracles do happen… now type that password, human.",
    "About time. Don’t get used to this level of responsibility. Password next.",
    "Bravo. You’ve met the minimal expectation of a functioning human. Password, please.",
    "Finally, some cooperation! Just the password and we’ll be done here.",
    "Yes! I can feel your excitement from here. Now, password time.",
    "I was getting tired of judging silently. Enter your password so I can stop sulking."
]

invalid_input_responses = [
    "Aurora: I said 'y' or 'n'. Not a novel, not hieroglyphs. Try again.",
    "Aurora: Yes or no. That’s it. I don’t do interpretive dance.",
    "Aurora: 'Y' or 'N'. Pick one, genius.",
    "Aurora: I can’t read your mind… yet. Use 'y' or 'n'.",
    "Aurora: Seriously? 'y' or 'n'… do you need me to hold your hand?",
    "Aurora: Not what I expected. 'y' or 'n', human.",
    "Aurora: You’re testing me. Answer 'y' or 'n', please.",
    "Aurora: Wrong input. I need 'y' or 'n'. Think fast.",
    "Aurora: I don’t speak gibberish. 'y' or 'n', try again.",
    "Aurora: That’s not even close. 'y' or 'n'. Focus!"
]

missing_contrib = [
    "Oh honey... you’re running this script without `pacman-contrib`? That’s like trying to use Tinder without profile pics. Anyway, fix your life with: `sudo pacman -S pacman-contrib`.",

    "Listen, champ. You forgot `pacman-contrib`. That’s like showing up to a gangbang without lube. Painful and embarrassing. Slam this into your terminal: `sudo pacman -S pacman-contrib`.",

    "Wow. You don’t have `pacman-contrib` installed. That’s like raw-dogging Arch without protection. Just wrap it up with: `sudo pacman -S pacman-contrib`.",

    "Congrats, genius. You managed to break the program by not installing `pacman-contrib`. That’s like trying to cook meth without a stove. Do yourself a favor: `sudo pacman -S pacman-contrib`.",

    "Oh my god. `pacman-contrib` isn’t installed. You’re literally edging yourself with broken software. Just nut already and type: `sudo pacman -S pacman-contrib`.",

    "Bruh. You didn’t install `pacman-contrib`? That’s like forgetting the condom *after* pulling out. Get your shit together: `sudo pacman -S pacman-contrib`.",

    "You absolute fucking menace. No `pacman-contrib`? That’s like going to a strip club and forgetting dollar bills. Fix your broke-ass with: `sudo pacman -S pacman-contrib`.",

    "Sweetheart, `pacman-contrib` is missing. That’s like masturbating with sandpaper. Painful, unnecessary, and weird. Just do this: `sudo pacman -S pacman-contrib`."
    
]