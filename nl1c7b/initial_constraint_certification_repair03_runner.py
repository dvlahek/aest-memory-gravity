#!/usr/bin/env python3
# Technical adapter for the preregistered Repair03 localization audit.
# H_SMALL_H is used by Repair03 only to report x=r/(R_sigma/h); it does not
# enter any field, action term, derivative, residual, normalization, or gate.
import nl1c7b.initial_constraint_certification as b4
import nl1c7b.initial_constraint_certification_repair03 as r3

b4.H_SMALL_H = 0.6733246390848661

if __name__ == '__main__':
    r3.main()
