package com.zakenchance.ai

import kotlin.math.max
import kotlin.random.Random

const val LOTTO_MIN = 1
const val LOTTO_MAX = 37
const val LOTTO_PICK_COUNT = 6
const val STRONG_MIN = 1
const val STRONG_MAX = 7

val ALL_LOTTO_NUMBERS = (LOTTO_MIN..LOTTO_MAX).toList()
val CHANCE_CARDS = listOf("7", "8", "9", "10", "J", "Q", "K", "A")
val CHANCE_SUITS = listOf("תלתן", "יהלום", "לב", "עלה")
private val HIGH_CARDS = setOf("J", "Q", "K", "A")
private val COMMON_HUMAN_NUMBERS = setOf(1, 2, 3, 4, 5, 7, 10, 11, 13, 18, 21, 22, 26, 30, 31)

data class LottoParseResult(
    val lottoNumbers: List<Int>,
    val strongNumbers: List<Int>,
    val invalidRows: List<String>,
)

data class ChanceParseResult(
    val draws: List<Map<String, String>>,
    val invalidRows: List<String>,
)

data class TicketScoreDetails(
    val score: Int,
    val evens: Int,
    val lows: Int,
    val total: Int,
    val adjacentPairs: Int,
    val penalties: List<String>,
)

data class GeneratedLottoTicket(
    val index: Int,
    val numbers: List<Int>,
    val strong: Int,
    val details: TicketScoreDetails,
)

fun parseLottoHistory(text: String): LottoParseResult {
    val lottoNumbers = mutableListOf<Int>()
    val strongNumbers = mutableListOf<Int>()
    val invalidRows = mutableListOf<String>()

    text.lines().forEachIndexed { rowIndex, line ->
        val cleaned = line.trim()
        if (cleaned.isEmpty()) {
            return@forEachIndexed
        }

        val parts = cleaned.split("|", limit = 2)
        if (parts.size != 2) {
            invalidRows += "שורה ${rowIndex + 1}: פורמט לא תקין (נדרש |)."
            return@forEachIndexed
        }

        val nums = parts[0].split(",").map { it.trim() }
        val strongToken = parts[1].trim()

        val parsedNums = nums.map { it.toIntOrNull() }
        val strong = strongToken.toIntOrNull()
        if (parsedNums.any { it == null } || strong == null) {
            invalidRows += "שורה ${rowIndex + 1}: ערכים חייבים להיות מספרים."
            return@forEachIndexed
        }

        val values = parsedNums.filterNotNull()
        if (values.size != LOTTO_PICK_COUNT) {
            invalidRows += "שורה ${rowIndex + 1}: חייבים בדיוק 6 מספרים."
            return@forEachIndexed
        }
        if (values.toSet().size != LOTTO_PICK_COUNT) {
            invalidRows += "שורה ${rowIndex + 1}: מספרים חייבים להיות ייחודיים."
            return@forEachIndexed
        }
        if (values.any { it !in LOTTO_MIN..LOTTO_MAX }) {
            invalidRows += "שורה ${rowIndex + 1}: טווח לוטו חייב להיות 1-37."
            return@forEachIndexed
        }
        if (strong !in STRONG_MIN..STRONG_MAX) {
            invalidRows += "שורה ${rowIndex + 1}: חזק חייב להיות בטווח 1-7."
            return@forEachIndexed
        }

        lottoNumbers += values
        strongNumbers += strong
    }

    return LottoParseResult(
        lottoNumbers = lottoNumbers,
        strongNumbers = strongNumbers,
        invalidRows = invalidRows,
    )
}

fun parseChanceHistory(text: String): ChanceParseResult {
    val draws = mutableListOf<Map<String, String>>()
    val invalidRows = mutableListOf<String>()

    text.lines().forEachIndexed { rowIndex, line ->
        val cleaned = line.trim()
        if (cleaned.isEmpty()) {
            return@forEachIndexed
        }

        val tokens = cleaned.split(",").map { it.trim().uppercase() }
        if (tokens.size != CHANCE_SUITS.size) {
            invalidRows += "שורה ${rowIndex + 1}: חייבים 4 קלפים לפי סדר הסמלים."
            return@forEachIndexed
        }

        if (tokens.any { it !in CHANCE_CARDS }) {
            invalidRows += "שורה ${rowIndex + 1}: קלפים חוקיים הם ${CHANCE_CARDS.joinToString(", ")}."
            return@forEachIndexed
        }

        draws += CHANCE_SUITS.zip(tokens).toMap()
    }

    return ChanceParseResult(draws = draws, invalidRows = invalidRows)
}

fun chanceSuitCounters(draws: List<Map<String, String>>): Map<String, Map<String, Int>> {
    return CHANCE_SUITS.associateWith { suit ->
        CHANCE_CARDS.associateWith { card ->
            draws.count { draw -> draw[suit] == card }
        }
    }
}

fun scoreTicket(numbers: List<Int>): TicketScoreDetails {
    val sorted = numbers.sorted()
    val evens = sorted.count { it % 2 == 0 }
    val lows = sorted.count { it <= 18 }
    val total = sorted.sum()
    val adjacent = sorted.zipWithNext().count { (a, b) -> b - a == 1 }

    var score = 100
    val penalties = mutableListOf<String>()

    if (evens !in setOf(2, 3, 4)) {
        score -= 20
        penalties += "איזון זוגי/אי-זוגי חלש"
    }
    if (lows !in setOf(2, 3, 4)) {
        score -= 20
        penalties += "יותר מדי נמוכים/גבוהים"
    }
    if (total !in 90..150) {
        score -= 20
        penalties += "סכום מחוץ לטווח 90-150"
    }
    if (adjacent > 1) {
        score -= 20
        penalties += "יותר מרצף אחד של מספרים עוקבים"
    }

    return TicketScoreDetails(
        score = max(0, score),
        evens = evens,
        lows = lows,
        total = total,
        adjacentPairs = adjacent,
        penalties = penalties,
    )
}

fun isAntiCrowd(numbers: List<Int>): Boolean {
    val birthdayCount = numbers.count { it <= 31 }
    val commonCount = numbers.count { it in COMMON_HUMAN_NUMBERS }
    return birthdayCount <= 4 && commonCount <= 2
}

private fun randomUniqueLotto(random: Random): List<Int> {
    return ALL_LOTTO_NUMBERS.shuffled(random).take(LOTTO_PICK_COUNT).sorted()
}

fun generateBalancedTicket(random: Random = Random.Default): List<Int> {
    var best = randomUniqueLotto(random)
    var bestScore = -1

    repeat(500) {
        val candidate = randomUniqueLotto(random)
        var candidateScore = scoreTicket(candidate).score
        if (isAntiCrowd(candidate)) {
            candidateScore += 15
        }
        if (candidateScore > bestScore) {
            bestScore = candidateScore
            best = candidate
        }
    }
    return best
}

fun generateHotColdTicket(lottoNumbers: List<Int>, random: Random = Random.Default): List<Int> {
    if (lottoNumbers.isEmpty()) {
        return generateBalancedTicket(random)
    }

    val counts = lottoNumbers.groupingBy { it }.eachCount()
    val hot = counts.entries.sortedByDescending { it.value }.take(12).map { it.key }
    val cold = ALL_LOTTO_NUMBERS.sortedBy { counts[it] ?: 0 }.take(12)

    val ticket = mutableSetOf<Int>()
    hot.shuffled(random).take(3).forEach { ticket += it }
    cold.shuffled(random).take(2).forEach { ticket += it }

    while (ticket.size < LOTTO_PICK_COUNT) {
        ticket += ALL_LOTTO_NUMBERS.random(random)
    }

    return ticket.toList().sorted()
}

fun chooseStrong(strongNumbers: List<Int>, random: Random = Random.Default): Int {
    if (strongNumbers.isEmpty()) {
        return random.nextInt(STRONG_MIN, STRONG_MAX + 1)
    }
    return strongNumbers.groupingBy { it }.eachCount().maxBy { it.value }.key
}

fun generateMultiTickets(
    amount: Int,
    mode: String,
    lottoNumbers: List<Int>,
    strongNumbers: List<Int>,
    random: Random = Random.Default,
): List<GeneratedLottoTicket> {
    val unique = linkedSetOf<List<Int>>()
    var attempts = 0
    val maxAttempts = amount * 1000

    while (unique.size < amount && attempts < maxAttempts) {
        attempts += 1

        val ticket = when (mode) {
            "Balanced Distribution" -> generateBalancedTicket(random)
            "Hot + Cold Mix" -> generateHotColdTicket(lottoNumbers, random)
            "Anti-Crowd Mode" -> {
                val candidate = generateBalancedTicket(random)
                if (!isAntiCrowd(candidate)) continue
                candidate
            }
            else -> randomUniqueLotto(random)
        }
        unique += ticket
    }

    return unique.mapIndexed { idx, numbers ->
        GeneratedLottoTicket(
            index = idx + 1,
            numbers = numbers,
            strong = chooseStrong(strongNumbers, random),
            details = scoreTicket(numbers),
        )
    }
}

private fun weightedChoice(items: List<String>, weights: List<Int>, random: Random): String {
    val normalizedWeights = if (weights.all { it <= 0 }) {
        List(weights.size) { 1 }
    } else {
        weights.map { if (it <= 0) 1 else it }
    }
    val totalWeight = normalizedWeights.sum()
    var pointer = random.nextInt(totalWeight)
    items.indices.forEach { idx ->
        pointer -= normalizedWeights[idx]
        if (pointer < 0) {
            return items[idx]
        }
    }
    return items.last()
}

fun generateBalancedChanceTicket(random: Random = Random.Default): Map<String, String> {
    repeat(200) {
        val pick = CHANCE_SUITS.associateWith { CHANCE_CARDS.random(random) }
        val values = pick.values
        val hasHigh = values.any { it in HIGH_CARDS }
        val hasLow = values.any { it !in HIGH_CARDS }
        if (values.toSet().size >= 3 && hasHigh && hasLow) {
            return pick
        }
    }
    return CHANCE_SUITS.associateWith { CHANCE_CARDS.random(random) }
}

fun generateHotColdChanceTicket(
    draws: List<Map<String, String>>,
    random: Random = Random.Default,
): Map<String, String> {
    if (draws.isEmpty()) {
        return generateBalancedChanceTicket(random)
    }

    val counters = chanceSuitCounters(draws)
    val ticket = mutableMapOf<String, String>()

    CHANCE_SUITS.forEach { suit ->
        val suitCounter = counters[suit].orEmpty()
        val hot = suitCounter.entries.sortedByDescending { it.value }.take(3).map { it.key }
        val cold = CHANCE_CARDS.sortedBy { suitCounter[it] ?: 0 }.take(3)
        val strategy = weightedChoice(
            items = listOf("hot", "cold", "random"),
            weights = listOf(4, 3, 2),
            random = random,
        )

        ticket[suit] = when (strategy) {
            "hot" -> (if (hot.isEmpty()) CHANCE_CARDS else hot).random(random)
            "cold" -> (if (cold.isEmpty()) CHANCE_CARDS else cold).random(random)
            else -> CHANCE_CARDS.random(random)
        }
    }
    return ticket
}

fun generateHistoryWeightedChanceTicket(
    draws: List<Map<String, String>>,
    random: Random = Random.Default,
): Map<String, String> {
    if (draws.isEmpty()) {
        return generateBalancedChanceTicket(random)
    }

    val counters = chanceSuitCounters(draws)
    return CHANCE_SUITS.associateWith { suit ->
        val suitCounter = counters[suit].orEmpty()
        val weights = CHANCE_CARDS.map { card -> (suitCounter[card] ?: 0) + 1 }
        weightedChoice(CHANCE_CARDS, weights, random)
    }
}

fun generateMultiChanceTickets(
    amount: Int,
    mode: String,
    draws: List<Map<String, String>>,
    random: Random = Random.Default,
): List<Map<String, String>> {
    val unique = linkedSetOf<List<String>>()
    var attempts = 0
    val maxAttempts = amount * 1000

    while (unique.size < amount && attempts < maxAttempts) {
        attempts += 1

        val ticket = when (mode) {
            "Balanced Distribution" -> generateBalancedChanceTicket(random)
            "History Weighted" -> generateHistoryWeightedChanceTicket(draws, random)
            "Hot + Cold Mix" -> generateHotColdChanceTicket(draws, random)
            else -> CHANCE_SUITS.associateWith { CHANCE_CARDS.random(random) }
        }
        unique += CHANCE_SUITS.map { suit -> ticket[suit].orEmpty() }
    }

    return unique.map { values ->
        CHANCE_SUITS.zip(values).toMap()
    }
}

fun lottoCsv(tickets: List<GeneratedLottoTicket>): String {
    val rows = mutableListOf(
        "ticket_index,numbers,strong,ai_score,evens,low_numbers,sum,adjacent_pairs,penalties",
    )
    tickets.forEach { ticket ->
        val penaltyText = if (ticket.details.penalties.isEmpty()) {
            "ללא הורדות"
        } else {
            ticket.details.penalties.joinToString("; ")
        }
        rows += listOf(
            ticket.index.toString(),
            ticket.numbers.joinToString("-"),
            ticket.strong.toString(),
            ticket.details.score.toString(),
            ticket.details.evens.toString(),
            ticket.details.lows.toString(),
            ticket.details.total.toString(),
            ticket.details.adjacentPairs.toString(),
            "\"$penaltyText\"",
        ).joinToString(",")
    }
    return rows.joinToString("\n")
}

fun chanceCsv(tickets: List<Map<String, String>>): String {
    val rows = mutableListOf("ticket_index,${CHANCE_SUITS.joinToString(",")}")
    tickets.forEachIndexed { idx, ticket ->
        val values = CHANCE_SUITS.map { suit -> ticket[suit].orEmpty() }
        rows += (listOf((idx + 1).toString()) + values).joinToString(",")
    }
    return rows.joinToString("\n")
}
