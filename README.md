# `hypothesis-6.100.8`

```
==================================================== FAILURES =====================================================
____________________________________________________ test_main ____________________________________________________

    @given(
>       data=data(),
        shape=array_shapes(),
        min_size=integers(0, 100),
        max_size=integers(0, 100) | none(),
    )

src/tests/test_main.py:32:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
.direnv/python-3.12/lib/python3.12/site-packages/hypothesis/internal/conjecture/engine.py:693: in run
    self._run()
.direnv/python-3.12/lib/python3.12/site-packages/hypothesis/internal/conjecture/engine.py:1142: in _run
    self.generate_new_examples()
.direnv/python-3.12/lib/python3.12/site-packages/hypothesis/internal/conjecture/engine.py:987: in generate_new_examples
    self.generate_mutations_from(data)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

self = <hypothesis.internal.conjecture.engine.ConjectureRunner object at 0x10fc01eb0>
data = ConjectureData(INVALID, 11 bytes, frozen)

    def generate_mutations_from(
        self, data: Union[ConjectureData, ConjectureResult]
    ) -> None:
        # A thing that is often useful but rarely happens by accident is
        # to generate the same value at multiple different points in the
        # test case.
        #
        # Rather than make this the responsibility of individual strategies
        # we implement a small mutator that just takes parts of the test
        # case with the same label and tries replacing one of them with a
        # copy of the other and tries running it. If we've made a good
        # guess about what to put where, this will run a similar generated
        # test case with more duplication.
        if (
            # An OVERRUN doesn't have enough information about the test
            # case to mutate, so we just skip those.
            data.status >= Status.INVALID
            # This has a tendency to trigger some weird edge cases during
            # generation so we don't let it run until we're done with the
            # health checks.
            and self.health_check_state is None
        ):
            initial_calls = self.call_count
            failed_mutations = 0

            while (
                self.should_generate_more()
                # We implement fairly conservative checks for how long we
                # we should run mutation for, as it's generally not obvious
                # how helpful it is for any given test case.
                and self.call_count <= initial_calls + 5
                and failed_mutations <= 5
            ):
                groups = data.examples.mutator_groups
                if not groups:
                    break

                group = self.random.choice(groups)

                ex1, ex2 = (
                    data.examples[i] for i in sorted(self.random.sample(group, 2))
                )
                assert ex1.end <= ex2.start

                e = self.random.choice([ex1, ex2])
                replacement = data.buffer[e.start : e.end]

                try:
                    # We attempt to replace both the examples with
                    # whichever choice we made. Note that this might end
                    # up messing up and getting the example boundaries
                    # wrong - labels matching are only a best guess as to
                    # whether the two are equivalent - but it doesn't
                    # really matter. It may not achieve the desired result,
                    # but it's still a perfectly acceptable choice sequence
                    # to try.
                    new_data = self.cached_test_function(
                        data.buffer[: ex1.start]
                        + replacement
                        + data.buffer[ex1.end : ex2.start]
                        + replacement
                        + data.buffer[ex2.end :],
                        # We set error_on_discard so that we don't end up
                        # entering parts of the tree we consider redundant
                        # and not worth exploring.
                        error_on_discard=True,
                        extend=BUFFER_SIZE,
                    )
                except ContainsDiscard:
                    failed_mutations += 1
                    continue

>               assert isinstance(new_data, ConjectureResult)
E               assert False
E                +  where False = isinstance(Overrun, ConjectureResult)

.direnv/python-3.12/lib/python3.12/site-packages/hypothesis/internal/conjecture/engine.py:1075: AssertionError

```
