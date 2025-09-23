
function Show-WeeklyProgress {
  [CmdletBinding()]
  param()

  $today = Get-Date
  $weekday = $today.DayOfWeek
  $dayOfWeek = [int]$today.DayOfWeek

  # Define comments for each workday
  $comments = @{
    1 = "Another week begins; brace yourself for the grind."      # Monday
    2 = "Keep your head down; survival is the name of the game."   # Tuesday
    3 = "You're halfway through, but the struggle is far from over." # Wednesday
    4 = "The end is in sight, but the battle rages on."            # Thursday
    5 = "It's Friday—time to reflect on the chaos of the week."    # Friday
}

  # Calculate completed days (1 for Monday to 5 for Friday)
  $completedDays = if ($dayOfWeek -ge 1) { $dayOfWeek } else { 0 }

  $totalDays = 5
  $percentComplete = ($completedDays / $totalDays) * 100

  # Get the comment for the current day
  $comment = if ($dayOfWeek -ge 1 -and $dayOfWeek -le 5) { $comments[$dayOfWeek] } else { "It's the weekend! Why are you working?!? Go back to sleep!" }

  # Display weekly progress with day number and comment
  Write-Host "Day $dayOfWeek - $weekday : $percentComplete% of the Week. $comment"
}

function Show-YearlyProgress {
  [CmdletBinding()]
  param()

  $date = Get-Date
  $culture = [System.Globalization.CultureInfo]::CurrentCulture
  $calendar = $culture.Calendar
  $weekNumber = $calendar.GetWeekOfYear($date, $culture.DateTimeFormat.CalendarWeekRule, $culture.DateTimeFormat.FirstDayOfWeek)
  
  # Get the current month and its number
  $monthNumber = $date.Month
  $monthName = $date.ToString("MMMM")

  # Define dark and gritty remarks for each month
  $monthRemarks = @{
    1 = "A cold reminder that the year is just beginning, and so are the struggles."
    2 = "The shortest month, yet it feels like an eternity in the depths of winter."
    3 = "Spring is near, but the chill of despair still lingers."
    4 = "Showers bring May flowers, but they also wash away hope."
    5 = "The promise of summer is tainted by the weight of unfulfilled dreams."
    6 = "The days grow longer, but so do the shadows of doubt."
    7 = "The heat is unbearable, much like the pressure of expectations."
    8 = "The end of summer approaches, and with it, the return of reality."
    9 = "A new season begins, but the cycle of struggle continues."
    10 = "The leaves fall, and so do our ambitions."
    11 = "A time for reflection, but all we see are the ghosts of our failures."
    12 = "The year ends, but the burdens we carry never truly fade."
  }

  $totalWeeks = 52
  $percentComplete = [math]::Round(($weekNumber / $totalWeeks) * 100)

  # Get the remark for the current month
  $monthRemark = if ($monthRemarks.ContainsKey($monthNumber)) { $monthRemarks[$monthNumber] } else { "Another month lost in the abyss." }

  # Display yearly progress with week number, month, and remark
  Write-Host "Week $weekNumber - $monthName : $percentComplete% of the Year. $monthRemark"
}


function Show-DailyProgress {
  $currentTime = Get-Date
  $startTime = Get-Date -Hour 9 -Minute 0 -Second 0
  $targetTime = Get-Date -Hour 18 -Minute 0 -Second 0
  $totalSeconds = ($targetTime - $startTime).TotalSeconds
  $remainingTime = New-TimeSpan -Start $currentTime -End $targetTime

  if ($currentTime.Hour -lt 9) {
    $remainingTime = $startTime - $currentTime
    $remainingHours = $remainingTime.Hours
    $remainingMinutes = $remainingTime.Minutes
    $remainingSeconds = $remainingTime.Seconds
    Write-Host ("Too early to work! Come back in {0:00}:{1:00}:{2:00}" -f $remainingHours, $remainingMinutes, $remainingSeconds)
  } elseif ($remainingTime.TotalSeconds -gt 0 -or $currentTime.Hour -lt 9) {
    while ($remainingTime.TotalSeconds -gt 0) {
      $currentTime = Get-Date
      $remainingTime = New-TimeSpan -Start $currentTime -End $targetTime
      $elapsedTime = $currentTime - $startTime
      $progress = [Math]::Floor(($elapsedTime.TotalSeconds / $totalSeconds) * 100)
      if ($progress -gt 100) {
        $progress = 100
      }

      $hours = [Math]::Floor($remainingTime.TotalSeconds / 3600)
      $minutes = [Math]::Floor(($remainingTime.TotalSeconds % 3600) / 60)
      $seconds = [Math]::Floor($remainingTime.TotalSeconds % 60)

      Write-Progress -Activity "Workday" -Status "$progress% Complete" -PercentComplete $progress
      Write-Host ("Countdown: {0:00}:{1:00}:{2:00}" -f $hours, $minutes, $seconds) -NoNewline
      Start-Sleep -s 1
      Write-Host "`r" -NoNewline # overwrite the previous line
    }
    shutdown /h
  }
    elseif ($remainingTime.TotalSeconds -lt 0) {
      $response = Read-Host "The shift is over! Can I Hibernate? (y/n)"
      if ($response -eq "y") {
        shutdown /h
      } else {
        Write-Host "Gotta crunch those extra hours!!!"
      }
  } else {
    Write-Host "The target time has already passed or it's too early."
    Write-Output $remainingTime.TotalSeconds
}

}

Show-YearlyProgress
Show-WeeklyProgress
Show-DailyProgress