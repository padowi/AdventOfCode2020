BEGIN {
    RS="\n\n";
    FS="[ \n]";
    split("byr,iyr,eyr,hgt,hcl,ecl,pid", required, ",");
    valid = 0
}

{
    for (i = 1; i <= NF; i++)
    {
        split($i, pair, ":");
        passports[NR][pair[1]] = pair[2]
    }
    score = 0
    for (req in required) {
        if (required[req] in passports[NR]) { score++; }
    }
    if (score == 7) { valid++ }
}

END {
    print(valid);
}
