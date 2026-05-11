package com.zakenchance.ai

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.random.Random

class ZakenChanceEngineTest {

    @Test
    fun `parse lotto history validates rows`() {
        val raw = """
            1,7,19,22,27,34 | 5
            1,1,2,3,4,5 | 2
            3,10,16,24,31,37 | 9
            3,10,16,24,31,37 | 2
        """.trimIndent()

        val result = parseLottoHistory(raw)

        assertEquals(12, result.lottoNumbers.size)
        assertEquals(listOf(5, 2), result.strongNumbers)
        assertEquals(2, result.invalidRows.size)
    }

    @Test
    fun `score ticket returns expected penalties`() {
        val details = scoreTicket(listOf(1, 2, 3, 4, 5, 6))
        assertEquals(40, details.score)
        assertEquals(3, details.penalties.size)
    }

    @Test
    fun `generate multi lotto tickets produces unique size`() {
        val tickets = generateMultiTickets(
            amount = 5,
            mode = "Random",
            lottoNumbers = emptyList(),
            strongNumbers = emptyList(),
            random = Random(123),
        )

        assertEquals(5, tickets.size)
        assertEquals(5, tickets.map { it.numbers }.toSet().size)
        assertTrue(tickets.all { it.numbers.size == 6 })
    }

    @Test
    fun `parse chance history validates row length and values`() {
        val raw = """
            10,K,8,J
            7,10,Q,A
            X,1,2,3
            7,8,9
        """.trimIndent()

        val result = parseChanceHistory(raw)
        assertEquals(2, result.draws.size)
        assertEquals(2, result.invalidRows.size)
    }
}
