---
layout: post
title:  "My Bash Prompt"
date:   2014-03-22 11:43:54
categories: Bash
---

This is the PS1 line I use on my laptop. It has every usefull information I need to get along with my work.

{% codeblock lang:bash %}
export PS1="\$(battery_status) "$Color_Off'$(git branch &>/dev/null;\
if [ $? -eq 0 ]; then \
  echo "$(echo `git status` | grep "nothing to commit" > /dev/null 2>&1; \
  if [ "$?" -eq "0" ]; then \
    # @4 - Clean repository - nothing to commit
    echo " '$BICyan$PathShort$Color_Off$BIBlue' git:('$BIGreen'"$(__git_ps1 "%s")"'$BIBlue')'$BIGreen' ✓"; \
  else \
    # @5 - Changes to working tree
    echo "'$BICyan$PathShort$Color_Off$BIBlue' git:('$BIRed'"$(__git_ps1 "%s")"'$BIBlue')'$BIRed' ✗"; \
  fi) \n'$Color_Off'=> "; \
else \
  # @2 - Prompt when not in GIT repo
  echo " '$BICyan$PathShort$Color_Off'\n'$Color_Off'=> "; \
fi)'
{% endcodeblock %}

The colors for the prompt are by [Mike Stewart](http://mediadoneright.com/content/ultimate-git-ps1-bash-prompt)

Battery status is a small crude ruby script that uses acpi

{% codeblock lang:bash %}
O="\033[0m"
R="\033[1;91m"        # Red
G="\033[1;92m"      # Green
Y="\033[1;93m"     # Yellow
W="\033[1;97m"      # White
 
acpi = 'acpi'.to_s.chomp
status = acpi.split(',')[0].downcase
charge = acpi.split(',')[1].to_i
 
if status.match('full')
        puts 'echo "#{W}[#{charge} =]#{O}"'
elsif status.match("discharging")
        if charge <100 && charge >=80
                puts 'echo "#{G}[#{charge} -]"'
        elsif charge >= 50 && charge <80
                puts 'echo "#{G}[#{charge} -]"'
        elsif charge < 50 && charge >30
                puts 'echo "#{Y}[#{charge} -]"'
        else
                puts 'echo "#{R}[#{charge} -]"'
        end
elsif status.match("charging")
        if charge >= 80
                puts 'echo "#{G}[#{charge} +]"'
        elsif charge <= 50 && charge >= 30
                puts 'echo "#{Y}[#{charge} +]"'
        else
                puts 'echo "#{R}[#{charge} +]"'
        end
end
{% endcodeblock %}
